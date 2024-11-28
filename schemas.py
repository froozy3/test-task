from pydantic import BaseModel, Field
from typing import List, Optional


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: str
    complete: Optional[bool] = False


class TargetUpdate(BaseModel):
    target_id: int
    notes: Optional[str] = None
    complete: Optional[bool] = None


class MissionCreate(BaseModel):
    cat_id: int
    complete: Optional[bool] = False
    targets: List[TargetCreate]


class MissionUpdate(BaseModel):
    complete: Optional[bool]
    targets: Optional[List[TargetUpdate]]
