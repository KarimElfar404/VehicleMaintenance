from pydantic import BaseModel, Field, EmailStr
from schemas.roles import RoleResponse
from datetime import date
class UserRegister(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=8)
    dob: date
    personal_id: str
    address: str
    blood_type: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    dob: date
    blood_type: str
    personal_id: str
    address: str
    role: RoleResponse

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    dob: date | None = None
    personal_id: str | None = None
    address: str | None = None
    blood_type: str | None = None
    role_id: int | None = None
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


