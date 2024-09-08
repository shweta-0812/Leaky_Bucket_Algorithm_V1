from pydantic import BaseModel
from enum import Enum
from typing import Dict, Any


class JobSchema(BaseModel):
    id: int
    job_priority: int = 1
    job_type: int
    job_publisher: str
    data: str = ""


class JobTypeEnum(Enum):
    IO_BASED = 1
    CPU_BASED = 2
