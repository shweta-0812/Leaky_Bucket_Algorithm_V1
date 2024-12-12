from pydantic import BaseModel
from enum import Enum, IntEnum
from typing import Dict, Any




class FruitEnum(str, Enum):
    pear = 'pear'
    banana = 'banana'


class ToolEnum(IntEnum):
    spanner = 1
    wrench = 2


class CookingModel(BaseModel):
    fruit: FruitEnum = FruitEnum.pear
    tool: ToolEnum = ToolEnum.spanner



class JobTypeEnum(IntEnum):
    IO_BASED = 1
    CPU_BASED = 2


class JobPublisherEnum(str, Enum):
    MOBILE = 'mobile'
    WEB = 'web'


class JobSchema(BaseModel):
    id: int
    job_priority: int = 1
    job_type: JobTypeEnum = JobTypeEnum.IO_BASED
    job_publisher: JobPublisherEnum = JobPublisherEnum.WEB
    data: str = ""
