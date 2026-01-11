from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

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
    diagnosis: str
    notes: str
    created_at: datetime
    patient: UserShort
    doctor: UserShort   
    
    model_config = ConfigDict(from_attributes=True)


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

