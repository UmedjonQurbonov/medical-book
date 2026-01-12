from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.db.base import Base
from apps.models.users import User
from datetime import datetime
from sqlalchemy.sql import func



class MedicalRecord(Base):
    __tablename__ = 'medical_record'
    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"),nullable=True)
    diagnosis: Mapped[str | None] = mapped_column(String(100), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(150), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])



