from database.models import User
from fastapi import Depends
from core.security import get_current_user
from fastapi import HTTPException, status

ROLE_PERMISSIONS = {
    "admin": {
        "user:create",
        "user:delete",
        "user:update",
        "user:read",
        "role:create",
        "role:update",
        "role:delete",
        "role:read"
    },
    "user": {
        "user:read"
    }  
}

def require_permission(requiredperm: str):
    def permission_checker(currentuser: User = Depends(get_current_user)):
        role_name = currentuser.role.name if currentuser.role else None
        user_permissions = ROLE_PERMISSIONS.get(role_name.lower(), set())

        if requiredperm not in user_permissions:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authoreized")

        return currentuser
    return permission_checker