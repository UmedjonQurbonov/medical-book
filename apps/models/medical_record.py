from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from apps.db.base import Base
from apps.models.users import User
from datetime import datetime
from sqlalchemy.sql import func



class MedicalRecord(Base):
    __tablename__ = 'medical_record'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    diagnosis: Mapped[str] = mapped_column(String(100)) 
    notes: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())



