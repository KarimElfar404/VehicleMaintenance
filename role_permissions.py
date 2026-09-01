from database.models import User
from fastapi import Depends
from core.security import get_current_user
from fastapi import HTTPException, status



ROLE_PERMISSIONS = {
    "administrator": {
        "user:read",
        "user:update",
        "user:create",
        "user:delete",
        "driver:read",
        "driver:update",
        "driver:delete",
        "driver:create",
        "maintenance_category:read",
        "maintenance_category:update",
        "maintenance_category:create",
        "maintenance_category:delete",
        "maintenance_subcategory:read",
        "maintenance_subcategory:update",
        "maintenance_subcategory:create",
        "maintenance_subcategory:delete",
        "maintenance_history:read",
        "manual_maintenance:read",
        "manual_maintenance:update",
        "manual_maintenance:create",
        "manual_maintenance:delete",
        "vehicle:read",
        "vehicle:update",
        "vehicle:create",
        "vehicle:delete",
        "ticket:read",
        "ticket:update",
        "ticket:create",
        "ticketstatus:update",
        "role:read",
        "role:update",
        "role:create",
        "role:delete",
    },
    "driver": {
        "ticket:read",
        "ticket:update",
        "ticket:create",
        "ticket:update",
        "vehicle:read",
        "user:read",
        "maintenance_history:read",
    },
    "reviewer": {
        "user:read",
        "vehicle:read",
        "driver:read",
        "ticket:read",
        "ticketstatus:update",
        "maintenance_history:read",
        
    },
    "accountant": {
        "user:read",
        "ticket:read",
        "ticketstatus:update",
    },
    "maintenance_creator": {
        "maintenance_category:read",
        "maintenance_category:update",
        "maintenance_category:create",
        "maintenance_category:delete",
        "maintenance_subcategory:read",
        "maintenance_subcategory:update",
        "maintenance_subcategory:create",
        "maintenance_subcategory:delete",
    },
    "maintenance_entry": {
        "manual_maintenance:read",
        "manual_maintenance:create",
        "manual_maintenance:update",
        "manual_maintenance:delete",
    },
    "regular user": {
        "user:read",
    }
}

def require_permission(required_perm: str):
    def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.role or not current_user.role.name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role"
            )
        role_name = current_user.role.name.lower()
        user_permissions = ROLE_PERMISSIONS.get(role_name, set())
        if required_perm not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{required_perm}' required."
            )
        return current_user
    return permission_checker