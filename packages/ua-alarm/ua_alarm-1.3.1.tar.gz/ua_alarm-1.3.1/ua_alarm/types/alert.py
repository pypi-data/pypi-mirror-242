from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .active_alert import ActiveAlert
from ..enums import v2RegionType

class Alert(BaseModel):
    regionId: Optional[str]
    regionType: v2RegionType
    regionName: Optional[str]
    regionEngName: Optional[str]
    lastUpdate: datetime
    activeAlerts: Optional[List[ActiveAlert]]