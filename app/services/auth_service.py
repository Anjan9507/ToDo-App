from passlib.context import CryptContext
from fastapi import HTTPException
from psycopg2 import errors
from app.utils import format_phn_number
import secrets

from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_refresh_token():
    return secrets.token_hex(32)


def create_user(db, data):
    cursor = db.cursor()

    hash_pwd = hash_password(data.password)

    frmtd_phone = format_phn_number(data.phone)
    try:
        cursor.execute("""INSERT INTO users (name, email, phone, pwd_hash) VALUES (%s, %s, %s, %s) 
                       RETURNING id, name, email, phone""",
                       (data.name, data.email, frmtd_phone, hash_pwd))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=400,
                detail="Register Failed"
            )

        db.commit()

        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3]
        }
    except errors.UniqueViolation:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email or Phone already exists"
        )
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()

        
def login_user(db, data):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id, email, pwd_hash FROM users WHERE email = %s", (data.email,))

        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials"
            )
        
        user_id = row[0]
        email = row[1]
        hashed_password = row[2]

        if not verify_password(data.password, hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid Credentials"
            )
        
        access_token = create_access_token({
            "user_id": user_id,
            "email": email
        })

        cursor.execute("DELETE FROM refresh_tokens WHERE user_id = %s", (user_id,))

        refresh_token = generate_refresh_token()

        cursor.execute("INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (%s, %s, NOW() + INTERVAL '10 days')", (user_id, refresh_token))

        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def new_access_token(db, refresh_token: str):
    cursor = db.cursor()
    try:
        cursor.execute(
             """SELECT
                    user_id
                FROM refresh_tokens
                WHERE token = %s
                AND expires_at > NOW()
            """, (refresh_token,))
        
        token_data = cursor.fetchone()
        if not token_data:
            raise HTTPException(
                status_code=401,
                detail="Invalid Refresh Token"
            )
        
        user_id = token_data[0]

        cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))

        user_data = cursor.fetchone()
        if not user_data:
            raise HTTPException(
                status_code=400,
                detail="Invalid Request"
            )
        
        email = user_data[0]
        
        access_token = create_access_token({
            "user_id": user_id,
            "email": email
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def forgot_password(db, data):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = %s", (data.email,))

        user = cursor.fetchone()
        if not user:
            return {"message": "If account exists, reset link has been sent"}
        
        user_id = user[0]

        cursor.execute("DELETE FROM pwd_reset_tokens WHERE user_id = %s", (user_id,))

        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

        cursor.execute("INSERT INTO pwd_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)", 
                       (user_id, reset_token, expires_at))
        
        db.commit()

        return {
            "message": "If account exists, password reset token generated",
            "reset_token": reset_token
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def reset_password(db, data):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT user_id FROM pwd_reset_tokens WHERE token = %s AND expires_at > NOW() AND used = FALSE", 
                       (data.token,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired token"
            )
        
        user_id = row[0]

        hashed_pwd = hash_password(data.new_password)

        cursor.execute("UPDATE users SET pwd_hash = %s WHERE id = %s", (hashed_pwd, user_id))

        cursor.execute("UPDATE pwd_reset_tokens SET used = TRUE WHERE token = %s", (data.token,))

        db.commit()

        return {"message": "Password reset successfull"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        
