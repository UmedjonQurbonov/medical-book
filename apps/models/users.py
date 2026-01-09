from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from passlib.context import CryptContext
from apps.db.base import Base

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto"
)

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)  # <- добавлено
    role: Mapped[str] = mapped_column(String(15), default='patient')
