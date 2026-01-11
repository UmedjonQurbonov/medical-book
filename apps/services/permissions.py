from fastapi import Depends, HTTPException

from apps.models.users import User

from .user_dependencies import get_current_user


def admin_required(user: User = Depends(get_current_user)):
    if not user.role.name == 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')
    print(user.role.name)
    return user