from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from datetime import timedelta
from apps.models.medical_record import MedicalRecord
from apps.schemas.medicbookserializer import MedicalRecordUpdate, MedicalRecordOut

class MedicalRecordService:

    @staticmethod
    async def get_by_patient_id(
        patient_id: int,
        session: AsyncSession
    ) -> MedicalRecord:

        result = await session.execute(
            select(MedicalRecord)
            .options(
                selectinload(MedicalRecord.patient),
                selectinload(MedicalRecord.doctor),
            )
            .where(MedicalRecord.patient_id == patient_id)
        )

        record = result.scalars().first()

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Medical record not found"
            )

        return record

    @staticmethod
    async def update(
        record_id: int,
        data: MedicalRecordUpdate,
        session: AsyncSession
    ):
        result = await session.execute(
            select(MedicalRecord)
            .options(
                selectinload(MedicalRecord.patient),
                selectinload(MedicalRecord.doctor),
            )
            .where(MedicalRecord.id == record_id)
        )

        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")

        if data.diagnosis is not None:
            record.diagnosis = data.diagnosis

        if data.notes is not None:
            record.notes = data.notes

        await session.commit()
        await session.refresh(record)

        return record


