from pydantic import BaseModel
from datetime import datetime

class RegionAlarm(BaseModel):
    regionId: str
    startDate: datetime
    endDate: datetime
    duration: str
    alertType: str
    regionName: str
    isContinue: bool