from schemas.user import UserCreate

class DoctorUser(UserCreate):
    is_doctor: bool
    user_id: int
    doctor_specialty: str