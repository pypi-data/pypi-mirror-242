from pydantic import BaseModel, EmailStr


class UserEmail(BaseModel):
    email: EmailStr


class Username(BaseModel):
    username: str

class Users(BaseModel):
    email: EmailStr
    password: str
    username: str

class SignupUser(BaseModel):
    email: EmailStr
    password: str
    username: str


class SigninUser(BaseModel):
    email: EmailStr
    password: str
