from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from database.models import Driver, User, Role


def get_all_drivers(db: Session):
    statement = (
        select(User)
        .join(Role, User.role_id == Role.id)
        .options(joinedload(User.driver_profile))
        .where(Role.name.ilike("driver"))
    )
    return db.scalars(statement).unique().all()


def get_driver_by_user_id(db: Session, user_id: int):
    statement = (
        select(User)
        .join(Role, User.role_id == Role.id)
        .options(joinedload(User.driver_profile))
        .where(User.id == user_id, Role.name.ilike("driver"))
    )
    return db.scalars(statement).first()


def delete_driver(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    db.delete(driver)
    db.commit()


def update_driver(db: Session, user: User):
    db.commit()
    db.refresh(user)
    return user

def create_driver(db: Session, user:User) -> Driver:
    if not user.driver_profile:
        new_profile = Driver(
            user_id = user.id,
            license_number = "",
            license_expire = user.dob,
            driving_record_check = False,
            own_car = False,
            assigned_vehicle_check = False
        )
        db.add(new_profile)
        db.flush()
        user.driver_profile = new_profile
    return user.driver_profile