from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database.models import Role
from database.models import User


def get_all_roles(db: Session):
    statement = select(Role)
    return db.execute(statement).scalars().all()

def get_role_by_id(db: Session, roleid: int):
    return db.get(Role, roleid)

def get_role_by_name(db: Session, name: str):
    statement = (
        select(Role)
        .where(Role.name == name)
    )
    return db.execute(statement).scalar_one_or_none()

def create_role(db: Session, newrole: Role):
    db.add(newrole)
    db.commit()
    db.refresh(newrole)
    return newrole

def delete_role(db: Session, delrole: Role):
    db.delete(delrole)
    db.commit()
    return None

def update_role(db: Session, updaterole: Role):
    db.commit()
    db.refresh(updaterole)
    return updaterole