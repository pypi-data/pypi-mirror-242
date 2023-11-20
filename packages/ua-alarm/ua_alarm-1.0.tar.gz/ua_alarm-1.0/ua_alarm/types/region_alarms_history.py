from pydantic import BaseModel
from typing import Optional, List
from .region_alarm import RegionAlarm

class RegionAlarmsHistory(BaseModel):
    regionId: Optional[str]
    regionName: Optional[str]
    alarms: Optional[List[RegionAlarm]]