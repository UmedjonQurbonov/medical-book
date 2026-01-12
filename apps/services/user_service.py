from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from datetime import timedelta
from apps.models.users import User
from apps.schemas.userserializer import UserCreate, UserLogin
from apps.services.auth_service import verify_password, hash_password, create_access_token
from apps.models.medical_record import MedicalRecord


class UserService:

    @staticmethod
    async def register_user(
        data: UserCreate,
        session: AsyncSession,
        current_user: User
    ):

        if current_user.role != "doctor":
            raise HTTPException(status_code=403, detail="Only doctor can register patients")

        if await session.scalar(select(User).where(User.email == data.email)):
            raise HTTPException(status_code=400, detail="User with this email already exists")

        new_user = User(
            full_name=data.full_name,
            email=data.email,
            password=hash_password(data.password),
            role="patient"
        )
        session.add(new_user)
        await session.flush()
        
        medical_record = MedicalRecord(
            patient_id=new_user.id,
            doctor_id=current_user.id,
            diagnosis=None,
            notes=None
        )
        session.add(medical_record)

        await session.commit()
        await session.refresh(new_user)

        return new_user


    
    @staticmethod
    async def login_user(data: UserLogin, session: AsyncSession):
        
        result = await session.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail='User not found'
            )
        
        if not verify_password(data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail='Incorrect email or password'
            )
        
        access_token_expires = timedelta(minutes=120)
        access_token = create_access_token(
            {'sub': user.email,
             'user_id': user.id},
            expires_delta=access_token_expires
        )
        return {
            'user': user,
            'token': access_token
        }
        
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()