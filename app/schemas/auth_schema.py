from pydantic import BaseModel, EmailStr, Field

class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)
    password: str = Field(min_length=8)

class RegisterUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str = Field(min_length=10, max_length=15)


