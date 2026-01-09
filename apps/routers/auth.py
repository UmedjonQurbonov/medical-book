from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.database import get_session
from apps.schemas.userserializer import UserOut, UserCreate, UserLogin, TokenResponse
from apps.services.user_service import UserService
from apps.services.user_dependencies import get_current_user
from apps.models.users import User



user_router = APIRouter(prefix='/user')


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