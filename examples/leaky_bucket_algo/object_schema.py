from pydantic import BaseModel
from enum import Enum
from typing import Dict, Any


class JobSchema(BaseModel):
    id: int
    job_priority: int = 1
    job_type: int
    job_publisher: str
    data: str = ""

    def stringify_ints(self) -> Dict[str, Any]:
        """
        Convert all int fields in the model to strings.
        """

        def convert_ints(obj):
            if isinstance(obj, dict):
                return {k: (str(v) if isinstance(v, int) else convert_ints(v)) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_ints(item) for item in obj]
            else:
                return obj

        # Get the dict representation of the model and convert ints to strings
        return convert_ints(self.dict())


class JobType(Enum):
    IO_BASED = 1
    CPU_BASED = 2
