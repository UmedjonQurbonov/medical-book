from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload 
from fastapi import HTTPException
from datetime import timedelta
from apps.models.appointments import Appointments
from apps.schemas.medicbookserializer import AppointmentCreate, AppointmentOut, AppointmentUpdate

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
    
    @staticmethod
    async def get_by_id(appointment_id: int, session: AsyncSession):
        result = await session.execute(
            select(Appointments).where(Appointments.id == appointment_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_put(
        appointment_id: int,
        data: AppointmentCreate,
        session: AsyncSession
    ):
        appointment = await AppointmentService.get_by_id(appointment_id, session)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        appointment.patient_id = data.patient_id
        appointment.doctor_id = data.doctor_id
        appointment.complaints = data.complaints
        appointment.status = data.status

        await session.commit()
        await session.refresh(appointment)
        return appointment
    
    @staticmethod
    async def update_patch(
        appointment_id: int,
        data: AppointmentUpdate,
        session: AsyncSession
    ):
        appointment = await AppointmentService.get_by_id(appointment_id, session)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(appointment, field, value)

        await session.commit()
        await session.refresh(appointment)
        return appointment

    @staticmethod
    async def get_by_id(appointment_id: int, session: AsyncSession):
        result = await session.execute(
            select(Appointments)
            .options(
                selectinload(Appointments.patient),
                selectinload(Appointments.doctor),
            )
            .where(Appointments.id == appointment_id)
        )

        appointment = result.scalar_one_or_none()

        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

        return appointment
