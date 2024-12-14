from pydantic import BaseModel

class FileMessage(BaseModel):
    user_id: int
    action: str