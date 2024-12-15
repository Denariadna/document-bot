from pydantic import BaseModel
from typing import Optional

class FileMessage(BaseModel):
    user_id: int
    action: str
    file_name: Optional[str] = None