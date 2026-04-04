from passlib.context import CryptContext
from fastapi import HTTPException
from psycopg2 import errors
from app.utils import format_phn_number

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

        

        

