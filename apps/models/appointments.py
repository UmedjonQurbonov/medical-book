from sqlalchemy import Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from apps.db.base import Base
from apps.models.users import User
from datetime import datetime
from sqlalchemy.sql import func


class Appointments(Base):
    __tablename__ = 'appointments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    complaints: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(101))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


