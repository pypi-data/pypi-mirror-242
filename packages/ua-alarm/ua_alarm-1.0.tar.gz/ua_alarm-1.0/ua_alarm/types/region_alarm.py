from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegionAlarm(BaseModel):
    regionId: Optional[str]
    startDate: datetime
    endDate: datetime
    duration: str
    alertType: str
    regionName: Optional[str]
    isContinue: bool