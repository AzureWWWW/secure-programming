from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserUpdate
from core.utils import get_current_active_user
from models.user import User
from models.doctor import Doctor

router = APIRouter()


@router.put("/updateDoctor/")
def update_doctor(
    doctor_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):
    # Ensure that the logged-in user is a doctor and they are updating their own information
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.user_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update user fields dynamically
    if doctor_update.first_name:
        current_user.first_name = doctor_update.first_name
    if doctor_update.last_name:
        current_user.last_name = doctor_update.last_name
    if doctor_update.email:
        current_user.email = doctor_update.email
    if doctor_update.phone_number:
        current_user.phone_number = doctor_update.phone_number
    if doctor_update.doctor_specialty:
        doctor.doctor_specialty = doctor_update.doctor_specialty
    

    db.commit()
    db.refresh(current_user)  # Refresh the user object with updated values
    db.refresh(doctor)

    return {"message": "User updated successfully", "user": current_user}
