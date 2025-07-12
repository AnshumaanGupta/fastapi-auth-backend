from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    is_verified: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None

class MessageResponse(BaseModel):
    message: str
    success: bool
