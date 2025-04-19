from datetime import datetime
from schemas.user import UserCreate, UserUpdate

class DoctorUser(UserCreate):
    user_id: int
    doctor_specialty: str
    
# class DoctorUpdate(UserUpdate):
#     doctor_specialty: str
    
class AdminUpdateDoctor(UserUpdate):
    status_expiry : datetime = None