# includes pydantic models

from pydantic import BaseModel
from schemas.user import UserCreate    

class AdminUser(UserCreate):
    is_admin: bool
    user_id: int

# pydantic model for updating role
class RoleUpdate(BaseModel):
    new_role: str