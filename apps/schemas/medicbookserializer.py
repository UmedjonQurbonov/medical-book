from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    diagnosis: str
    notes: str

class UserShort(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class MedicalRecordOut(BaseModel):
    id: int
    diagnosis: Optional[str]
    notes: Optional[str]
    created_at: datetime
    patient: UserShort
    doctor: Optional[UserShort]

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    complaints: str
    status: str
    


class AppointmentOut(BaseModel):
    id: int
    patient: UserShort
    doctor: UserShort
    complaints: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AppointmentUpdate(BaseModel):
    complaints: Optional[str] = None
    status: Optional[str] = None

