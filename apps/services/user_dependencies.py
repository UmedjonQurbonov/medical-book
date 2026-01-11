from fastapi import Depends, HTTPException, status
from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from apps.db.database import get_session
from .auth_service import verify_token
from .user_service import UserService


security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession = Depends(get_session)):    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(credentials)
    token = credentials.credentials
    payload = verify_token(token)
    email: str = payload.get("sub")
    print(email)
    if email is None:
        raise credentials_exception
    
    user = await UserService.get_user_by_email(db=session, email=email)
    if user is None:
        raise credentials_exception
    
    return user