from passlib.context import CryptContext
from fastapi import HTTPException
from psycopg2 import errors
from app.utils import format_phn_number

from jose import jwt
from datetime import datetime, timedelta
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

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
    

