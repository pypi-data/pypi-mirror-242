from pydantic import BaseModel
from typing import Optional, List
from .region_view import RegionView

class RegionsView(BaseModel):
    states: Optional[List["RegionView"]]