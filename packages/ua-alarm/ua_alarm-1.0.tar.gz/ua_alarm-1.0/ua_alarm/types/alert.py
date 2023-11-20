from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .active_alert import ActiveAlert

class Alert(BaseModel):
    regionId: Optional[str]
    regionType: str
    regionName: Optional[str]
    regionEngName: Optional[str]
    lastUpdate: datetime
    activeAlerts: Optional[List[ActiveAlert]]