from pydantic import BaseModel

class FileMessage(BaseModel):
    id: int
    user_id: str
    action: str