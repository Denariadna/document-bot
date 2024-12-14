from pydantic import BaseModel

class AddFileRequest(BaseModel):
    user_id: int
    file_name: str
    file_path: str

class FileResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    created_at: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: str
