from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserUpdate
from core.utils import get_current_active_user
from models.user import User
from models.patient import Patient
import schemas
import schemas.user

router = APIRouter()

@router.put("/updateUser/")
def update_patient(
    patient_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):
    # Ensure that the logged-in user is a patient and they are updating their own information
    patient = db.query(Patient).filter(Patient.user_id == current_user.user_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Update user fields dynamically
    if patient_update.first_name:
        current_user.first_name = patient_update.first_name
    if patient_update.last_name:
        current_user.last_name = patient_update.last_name
    if patient_update.email:
        current_user.email = patient_update.email
    if patient_update.phone_number:
        current_user.phone_number = patient_update.phone_number

    db.commit()
    db.refresh(current_user)  # Refresh the user object with updated values

    return {"message": "User updated successfully", "user": current_user}
