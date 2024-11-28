from fastapi import APIRouter, Depends
from crud import set_spy_cat, update_spy_cat, remove_spy_cat, get_spy_cats, get_spy_cat
from models import get_db

cats_router = APIRouter()
SessionLocal = get_db()


@cats_router.post("/create")
def create(name: str, experience: int, breed: str, salary: float = None, session: SessionLocal = Depends(get_db)):
    set_spy_cat(session, name, experience, breed, salary)
    return {"message": "spy-cat created."}


@cats_router.get("/get-list")
def list_cats(session: SessionLocal = Depends(get_db)):
    return get_spy_cats(session)


@cats_router.get("/get-single")
def single_cat(id: int, session: SessionLocal = Depends(get_db)):
    return get_spy_cat(id, session)


@cats_router.patch("/update")
def update(id: int, salary: float = None, session: SessionLocal = Depends(get_db)):
    return update_spy_cat(session, id, salary)


@cats_router.delete("/delete")
def remove(id: int, session: SessionLocal = Depends(get_db)):
    return remove_spy_cat(id, session)
