from schemas.user import UserCreate

class PatientUser(UserCreate):
    is_patient: bool
    user_id: int