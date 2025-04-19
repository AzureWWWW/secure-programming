from schemas.user import UserCreate

class PatientUser(UserCreate):
    user_id: int