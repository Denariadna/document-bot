from pydantic import BaseModel

class FileMessage(BaseModel):
    action: str
    user_id: str
    file_name: str