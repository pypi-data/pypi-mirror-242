from pydantic import BaseModel
from typing import Optional, List

class RegionView(BaseModel):
    regionId: Optional[str]
    regionName: Optional[str]
    regionType: str
    regionChildIds: Optional[List["RegionView"]]