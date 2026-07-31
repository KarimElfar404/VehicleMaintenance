from fastapi import APIRouter, Depends
from schemas.roles import RoleCreate, RoleUpdate, RoleResponse
from database.database import get_db
from sqlalchemy.orm import Session
from services import roles_service
from fastapi import status
from schemas.users import UserResponse
from database.models import User
from role_permissions import require_permission
router = APIRouter()

@router.get("/role", response_model=list[RoleResponse], tags = ["Roles"])
def get_all_role(db: Session = Depends(get_db)):
    return roles_service.get_all_roles(db)

@router.get("/role/{roleid}", response_model=RoleResponse, tags = ["Roles"])
def get_role(roleid: int, db: Session = Depends(get_db)):
    return roles_service.get_role(db, roleid)

@router.post("/role",status_code=status.HTTP_201_CREATED ,tags = ["Roles"])
def create_role(newrole: RoleCreate, db: Session = Depends(get_db)):
    return roles_service.create_role(db, newrole)

@router.delete("/role/{roleid}" ,status_code=status.HTTP_204_NO_CONTENT, tags = ["Roles"])
def delete_role(roleid: int, current_user: User = Depends(require_permission("role:delete")) ,db: Session = Depends(get_db)):
    return roles_service.delete_role(db, roleid)

@router.patch("/role/{roleid}", status_code=status.HTTP_200_OK, tags = ["Roles"])
def update_role(roleid:int, updaterole: RoleUpdate, db:Session = Depends(get_db)):
    return roles_service.update_role(db, roleid, updaterole)

