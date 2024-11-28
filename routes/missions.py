from fastapi import APIRouter, Depends

from crud import create_mission, get_mission, remove_mission, update_mission, list_mission
from models import get_db
from schemas import MissionCreate, MissionUpdate, TargetUpdate

missions_router = APIRouter()
SessionLocal = get_db()


@missions_router.post("/create/", response_model=MissionCreate)
def create(mission: MissionCreate, session: SessionLocal = Depends(get_db)):
    return create_mission(mission, session)


@missions_router.get("/get-single")
def get_single_mission(id, session: SessionLocal = Depends(get_db)):
    return get_mission(id, session)


@missions_router.get("/get-list")
def get_list_mission(session: SessionLocal = Depends(get_db)):
    return list_mission(session)


@missions_router.patch("/update")
def update(mission_id: int, target_update: TargetUpdate, session: SessionLocal = Depends(get_db)):
    return update_mission(mission_id, target_update, session)


@missions_router.delete("/delete")
def remove(id: int, session: SessionLocal = Depends(get_db)):
    return remove_mission(id, session)
