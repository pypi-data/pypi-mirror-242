from pydantic import BaseModel
from datetime import datetime

class ActiveAlert(BaseModel):
    regionId: str
    regionType: str
    type: str
    lastUpdate: datetime