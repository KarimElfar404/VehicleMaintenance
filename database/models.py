from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    dob: Mapped[str] = mapped_column(nullable=False)
    personal_id: Mapped[str]
    address: Mapped[str]
    blood_type: Mapped[str] = mapped_column(nullable=False)