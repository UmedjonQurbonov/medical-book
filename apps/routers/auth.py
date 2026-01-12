from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.database import get_session
from apps.schemas.userserializer import UserOut, UserCreate, UserLogin, TokenResponse
from apps.schemas.medicbookserializer import AppointmentCreate, AppointmentOut, AppointmentUpdate, MedicalRecordOut, MedicalRecordUpdate
from apps.services.user_service import UserService
from apps.services.appointment_service import AppointmentService
from apps.services.medical_record_service import MedicalRecordService
from apps.services.user_dependencies import get_current_user
from apps.models.users import User
from apps.models.appointments import Appointments
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from apps.services.permissions import require_roles


user_router = APIRouter(prefix='/user')
appointment_router = APIRouter(prefix='/appointment')
medical_record_router = APIRouter(prefix='/medical_record')


@user_router.post("/register-patient", dependencies=[Depends(require_roles("admin", "doctor"))])
async def register_patient(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await UserService.register_user(data, session, current_user)


@user_router.post('/login/', response_model=TokenResponse)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await UserService.login_user(data=data, session=session)
    print(user)
    return {"access_token": user.get('token'), "token_type": "bearer"}

@user_router.get('/me/', response_model=UserOut)
async def profile(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    print(user)
    return user

@appointment_router.post('/create/', dependencies=[Depends(require_roles("doctor", "admin"))] ,status_code=status.HTTP_201_CREATED)
async def create(data: AppointmentCreate, session: AsyncSession = Depends(get_session)):
    appointment = await AppointmentService.create_appointment(data=data, session=session)
    return appointment

@appointment_router.get('/get/',response_model=list[AppointmentOut],status_code=status.HTTP_200_OK, dependencies=[Depends(require_roles("doctor", "admin"))])
async def get_appointments(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(select(Appointments).options(selectinload(Appointments.patient),selectinload(Appointments.doctor),)
    )
    return result.scalars().all()


@appointment_router.put("/{appointment_id}", response_model=AppointmentOut, dependencies=[Depends(require_roles("doctor", "admin"))])
async def update_appointment_put(
    appointment_id: int,
    data: AppointmentCreate,
    session: AsyncSession = Depends(get_session)
):
    return await AppointmentService.update_put(appointment_id, data, session)


@appointment_router.patch("/{appointment_id}", response_model=AppointmentOut, dependencies=[Depends(require_roles("doctor", "admin"))])
async def update_appointment_patch(
    appointment_id: int,
    data: AppointmentUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await AppointmentService.update_patch(appointment_id, data, session)


@appointment_router.delete("/{appointment_id}", status_code=204, dependencies=[Depends(require_roles("doctor", "admin"))])
async def delete_appointment(
    appointment_id: int,
    session: AsyncSession = Depends(get_session)
):
    await AppointmentService.delete(appointment_id, session)

@appointment_router.get(
    "/{appointment_id}",
    response_model=AppointmentOut,
    dependencies=[Depends(require_roles("doctor", "admin"))]
)
async def get_appointment_by_id(
    appointment_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await AppointmentService.get_by_id(appointment_id, session)  


@medical_record_router.get("/patient/{patient_id}", response_model=MedicalRecordOut, dependencies=[Depends(require_roles("doctor", "admin"))])
async def get_medical_record(
    patient_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await MedicalRecordService.get_by_patient_id(patient_id, session)

@medical_record_router.patch("/{record_id}", response_model=MedicalRecordOut, dependencies=[Depends(require_roles("doctor", "admin"))])
async def update_medical_record(
    record_id: int,
    data: MedicalRecordUpdate,
    user: User = Depends(require_roles("doctor", "admin")),
    session: AsyncSession = Depends(get_session),
):
    return await MedicalRecordService.update(record_id, data, session)


