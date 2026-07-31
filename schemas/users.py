from pydantic import BaseModel, Field, EmailStr

class UserRegister(BaseModel):
    name: str
    email: str
    hashed_password: str = Field(min_length=8)
    dob: str
    personal_id: str
    address: str
    blood_type: str

class UserResponse(BaseModel):
    name: str
    email: str
    dob: str
    blood_type: str
    personal_id: str
    address: str

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    dob: str | None = None
    personal_id: str | None = None
    address: str | None = None
    blood_type: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


