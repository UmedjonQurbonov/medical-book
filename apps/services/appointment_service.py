from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from datetime import timedelta
from apps.models.appointments import Appointments
from apps.schemas.medicbookserializer import AppointmentCreate, AppointmentOut

class AppointmentService:

    @staticmethod
    async def create_appointment(data: AppointmentCreate, session: AsyncSession):
        new_appoinment = Appointments(
            patient_id = data.patient_id,
            doctor_id = data.doctor_id,
            complaints = data.complaints,
            status = data.status
        )

        session.add(new_appoinment)
        await session.commit()
        await session.refresh(new_appoinment)
        return new_appoinment