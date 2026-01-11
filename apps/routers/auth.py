from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.database import get_session
from apps.schemas.userserializer import UserOut, UserCreate, UserLogin, TokenResponse
from apps.schemas.medicbookserializer import AppointmentCreate, AppointmentOut
from apps.services.user_service import UserService
from apps.services.appointment_service import AppointmentService
from apps.services.user_dependencies import get_current_user
from apps.models.users import User
from apps.models.appointments import Appointments
from sqlalchemy import select
from sqlalchemy.orm import selectinload


user_router = APIRouter(prefix='/user')
appointment_router = APIRouter(prefix='/appointment')


@user_router.post('/regiter/', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await UserService.register_user(data=data, session=session)
    return user

@user_router.post('/login/', response_model=TokenResponse)
async def login(data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await UserService.login_user(data=data, session=session)
    print(user)
    return {"access_token": user.get('token'), "token_type": "bearer"}

@user_router.get('/me/', response_model=UserOut)
async def profile(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    print(user)
    return user

@appointment_router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create(data: AppointmentCreate, session: AsyncSession = Depends(get_session)):
    appointment = await AppointmentService.create_appointment(data=data, session=session)
    return appointment

@appointment_router.get(
    '/get/',
    response_model=list[AppointmentOut],
    status_code=status.HTTP_200_OK
)
async def get_appointments(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    result = await session.execute(
        select(Appointments)
        .options(
            selectinload(Appointments.patient),
            selectinload(Appointments.doctor),
        )
    )
    return result.scalars().all()