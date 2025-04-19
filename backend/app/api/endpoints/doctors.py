from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
# from schemas.doctor import DoctorUpdate
from core.utils import isNameValid, isEmailValid, isPhoneNumberValid
from models.user import User
from models.doctor import Doctor

router = APIRouter()




def get_doctor_name_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doctor_id==doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    user = db.query(User).filter(User.user_id == doctor.user_id).first() 
    if not user:
        raise HTTPException(status_code=404, detail="Doctor is Not a User")
    return  f"{user.first_name} {user.last_name}"



def get_doctor_id_by_Name(doctor_name: str, db: Session = Depends(get_db)):
    if isNameValid(doctor_name) :
        raise HTTPException(status_code=400, detail="Invalid Doctor Name")
    user = db.query(User).filter(User.first_name == doctor_name.split(' ')[0],  User.last_name ==doctor_name.split(' ')[1]).first() 
    if not user:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    doctor = db.query(Doctor).filter(Doctor.user_id == user.user_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    return doctor.doctor_id

def get_doctor_id_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first() 
    if not user:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    doctor = db.query(Doctor).filter(Doctor.user_id== user.user_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    return doctor.patient_id



@router.get("/getAllDoctors/")
def get_all_doctors(db: Session = Depends(get_db)):
    info = []
    doctor_db = db.query(Doctor).all()
    for doctor in doctor_db:
        doctor_name = get_doctor_name_by_id(doctor.doctor_id,db)
        user = db.query(User).filter(User.user_id == doctor.user_id).first() 
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")
        app_data = {"doctor_id": doctor.doctor_id,
                    "doctor_name":doctor_name,
                     "username":user.username,
                     "status_expiry": doctor.status_expiry,
                     "email":user.email,
                     "phone_number": user.phone_number}
        info.append(app_data)
    return info

def isDoctorValid(user_id:int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.user_id==user_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    if doctor.is_patient == 0:
        return 0
    return doctor.doctor_id
