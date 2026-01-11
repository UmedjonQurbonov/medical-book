from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from datetime import timedelta
from apps.models.users import User
from apps.schemas.userserializer import UserCreate, UserLogin
from apps.services.auth_service import verify_password, hash_password, create_access_token


class UserService:

    @staticmethod
    async def register_user(data: UserCreate, session: AsyncSession):

        result = await session.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='User with this email already exists')

        result = await session.execute(select(User).where(User.full_name == data.full_name))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail='User with this fullname already exists')

        new_user = User(
            full_name=data.full_name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role 
        )
        session.add(new_user)
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