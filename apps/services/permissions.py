from apps.models.users import User
from .user_dependencies import get_current_user
from fastapi import Depends, HTTPException, status
from apps.services.user_dependencies import get_current_user
from apps.models.users import User


def admin_required(user: User = Depends(get_current_user)):
    if not user.role.name == 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')
    print(user.role.name)
    return user



def require_roles(*roles: str):
    async def checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission"
            )
        return user
    return checker