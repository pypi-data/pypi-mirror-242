from pydantic import BaseModel, EmailStr


class UserEmail(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@naver.com",
            }
        }


class Username(BaseModel):
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "도라에몽"
            }
        }


class SignupUser(BaseModel):
    email: EmailStr
    password: str
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@naver.com",
                "password": "test123!",
                "username": "도라에몽"
            }
        }


class SigninUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "test@naver.com",
                "password": "test123!",
            }
        }
