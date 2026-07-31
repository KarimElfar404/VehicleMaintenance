from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.roles import RoleCreate, RoleResponse, RoleUpdate
from database.models import Role
from repositories import roles_repository, users_repository
from sqlalchemy import select

def create_role(db: Session, newrole: RoleCreate):

    exist_role = roles_repository.get_role_by_name(db, newrole.name)

    if exist_role is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Role Is Already Created")
    
    db_role = Role(
        name = newrole.name
    )
    return roles_repository.create_role(db, db_role)

def get_role(db: Session, roleid: int):
    role = roles_repository.get_role_by_id(db, roleid)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Role not found")
    return role

def get_all_roles(db: Session):
    return roles_repository.get_all_roles(db)

def update_role(db: Session, roleid: int, updaterole: RoleUpdate):
    role = roles_repository.get_role_by_id(db, roleid)

    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Role is not Found")

    if updaterole.name is not None:
        role.name = updaterole.name

    return roles_repository.update_role(db, role)

def delete_role(db: Session, roleid: int):
    role = roles_repository.get_role_by_id(db, roleid)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Role is not Found")
    return roles_repository.delete_role(db, role)
