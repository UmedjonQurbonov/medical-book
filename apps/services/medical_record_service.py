from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from datetime import timedelta
from apps.models.medical_record import MedicalRecord
from apps.schemas.medicbookserializer import MedicalRecordCreate, MedicalRecordOut

class MedicalRecordService:

    @staticmethod
    async def create_medeical_record(data: MedicalRecordCreate, session: AsyncSession):
        result = await session.execute(select(MedicalRecord).where(MedicalRecord.patient_id == data.patient_id))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='Patient alredy have Medical Record')
        new_medical_record = MedicalRecord(
            patient_id = data.patient_id,
            doctor_id = data.doctor_id,
            diagnosis = data.diagnosis,
            notes = data.notes
        )    

