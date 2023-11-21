from pydantic import BaseModel
from typing import Optional, List
from ..enums import v2RegionType

class RegionView(BaseModel):
    regionId: Optional[str]
    regionName: Optional[str]
    regionType: v2RegionType
    regionChildIds: Optional[List["RegionView"]]