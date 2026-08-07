from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    dob: Mapped[str] = mapped_column(nullable=False)
    personal_id: Mapped[str]
    address: Mapped[str]
    blood_type: Mapped[str] = mapped_column(nullable=False)

    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default = 1, nullable = False)
    role: Mapped["Role"] = relationship(back_populates="user")

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")