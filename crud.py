from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from schemas import MissionCreate, TargetUpdate
from utils import validate_beer
from models import SpyCat, get_db, Mission, Target

SessionLocal = get_db()


# for SpyCat
def set_spy_cat(session: SessionLocal, name: str, experience: int, breed: str, salary: float = None):
    existing_name = session.query(SpyCat).filter(SpyCat.name == name).first()

    if existing_name:
        raise HTTPException(status_code=400, detail="Cat with name already exist")
    if not name or experience < 0:
        raise HTTPException(status_code=400, detail="Invalid input data")
    if not validate_beer(breed):
        raise HTTPException(status_code=404, detail="Invalid breed")
    try:
        new_cat = SpyCat(name=name, years_of_experience=experience, breed=breed, salary=salary)
        session.add(new_cat)
        session.commit()
        return new_cat
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving the cat to the database: {str(e)}")


def get_spy_cats(session: SessionLocal):
    return session.query(SpyCat).all()


def get_spy_cat(id: int, session: SessionLocal):
    spy_cat = session.get(SpyCat, id)
    if not spy_cat:
        raise HTTPException(status_code=404, detail="Invalid id. Cat not found.")

    return spy_cat


def update_spy_cat(session: SessionLocal, id: int, salary: float):
    spy_cat = session.get(SpyCat, id)

    if not spy_cat:
        raise HTTPException(status_code=404, detail="Invalid id. Cat not found.")

    try:
        spy_cat.salary = salary
        session.commit()
        return session.get(SpyCat, id)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving the cat to the database: {str(e)}")


def remove_spy_cat(id, session: SessionLocal):
    spy_cat = session.get(SpyCat, id)
    if not SpyCat:
        raise HTTPException(status_code=404, detail="Invalid id. Cat not found.")
    session.delete(spy_cat)
    session.commit()
    return {"message": "Spy successfully deleted."}


# for Mission

def create_mission(mission: MissionCreate, session: SessionLocal):
    cat = session.get(SpyCat, mission.cat_id)

    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    try:
        db_mission = Mission(cat_id=mission.cat_id, complete=mission.complete)
        session.add(db_mission)
        session.commit()
        session.refresh(db_mission)

        for target in mission.targets:
            db_target = Target(name=target.name, country=target.country,
                               notes=target.notes,
                               complete=target.complete, mission_id=db_mission.id)
            session.add(db_target)

        session.commit()
        return db_mission

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating mission: {str(e)}")


def update_mission(mission_id: int, target_update: TargetUpdate, session: SessionLocal):
    db_targets = session.query(Target).filter(Target.mission_id == mission_id).all()

    if not db_targets:
        raise HTTPException(status_code=404, detail="Target not found")

    db_mission = session.get(Mission, mission_id)

    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    mission_complete = db_mission.complete

    updated_targets = []
    for db_target in db_targets:
        if db_target.id == target_update.target_id:

            if db_target.complete or mission_complete:
                raise HTTPException(status_code=403, detail="Target or mission already completed")

            if target_update.complete is not None:
                db_target.complete = target_update.complete

            if target_update.notes is not None:
                db_target.notes = target_update.notes

            updated_targets.append(db_target)

    if updated_targets:
        if all(t.complete for t in db_targets):
            db_mission = session.get(Mission, mission_id)
            if db_mission:
                db_mission.complete = True

        try:
            session.commit()
            session.refresh(session.get(Target, target_update.target_id))
            return session.get(Target, target_update.target_id)
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail="Target with specified target_id not found")


def list_mission(session: SessionLocal):
    return session.query(Mission).all()


def get_mission(id: int, session: SessionLocal):
    mission = session.get(Mission, id)
    if not mission:
        raise HTTPException(status_code=404, detail="Invalid id. Cat not found.")

    return mission


def remove_mission(id: int, session: SessionLocal):
    mission = session.get(Mission, id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found.")

    if mission.cat_id is not None:
        raise HTTPException(status_code=403, detail="Mission cannot be deleted because it is assigned to a cat")
    try:
        session.delete(mission)
        session.commit()
    except Exception as e:
        session.rollback()
        HTTPException(status_code=500, detail=str(e))

    return {"message": "Mission successfully deleted!"}
