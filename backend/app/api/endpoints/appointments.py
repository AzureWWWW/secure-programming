from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from schemas.appointment import AppointmentCreate, AdminAppointmentUpdate, UserAppointmentUpdate
from models.appointment import Appointment
from models.user import User
from .patients import get_patient_name_by_id, get_patient_id_by_Name, get_patient_id_by_user_id, isPatientValid
from .doctors import get_doctor_name_by_id, get_doctor_id_by_Name, get_doctor_id_by_user_id, isDoctorValid
from core.utils import Is_User_Valid, get_current_user, get_current_admin

router = APIRouter()

allowed_status = ['SCHEDULED', 'CANCELLED', 'CONFIRMED', 'IN PROGRESS', 'COMPLETED', 'CONFIRMED']
@router.post("/addAppointment/")
def create_appointment(user_data: AppointmentCreate, db: Session = Depends(get_db)):
    #check patient_id and doctor_id exist
    patient_validity = Is_User_Valid(user_data.patient_id, "patient",db)
    doctor_validity = Is_User_Valid(user_data.doctor_id, "doctor",db)
    if patient_validity == False :
        raise HTTPException(status_code=404, detail="Patient Not Found")
    elif doctor_validity == False:
        raise HTTPException(status_code=404, detail="Doctor Not Found")
    db_appointment = Appointment(patient_id = user_data.patient_id, doctor_id= user_data.doctor_id, description = user_data.description, date_time = user_data.date_time )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {"message": "Appointment Successfully Added"}


@router.get("/getAllAppointments/")
def get_all_appointments(db: Session = Depends(get_db)):
    info = []
    appointment_db = db.query(Appointment).all()
    for appointment in appointment_db:
        patient_name = get_patient_name_by_id(appointment.patient_id,db)
        doctor_name = get_doctor_name_by_id(appointment.doctor_id,db)
        app_data = {"appointment_id": appointment.appointment_id,
                    "patient_name":patient_name,
                    "doctor_name":doctor_name,
                    "description":appointment.description,
                    "date_time":appointment.date_time,
                    "status": appointment.status }
        info.append(app_data)

    return info

@router.get("/getDoctorAppointments/{id}")
def getDoctorAppointments(id:int, db: Session = Depends(get_db)):
    info = []
    appointment_db = db.query(Appointment).all()
    for appointment in appointment_db:
        if appointment.doctor_id == id: 
            patient_name = get_patient_name_by_id(appointment.doctor_id,db)
            app_data = {"appointment_id": appointment.appointment_id,
                            "patient_name":patient_name,
                            "description":appointment.description,
                            "date_time":appointment.date_time,
                            "status": appointment.status }
            info.append(app_data)
    return info

@router.get("/getPatientAppointments/{id}")
def getDoctorAppointments(id:int, db: Session = Depends(get_db)):
    info = []
    appointment_db = db.query(Appointment).all()
    for appointment in appointment_db:
        if appointment.patient_id == id: 
            doctor_name = get_doctor_name_by_id(appointment.patient_id,db)
            app_data = {"appointment_id": appointment.appointment_id,
                            "doctor_name":doctor_name,
                            "description":appointment.description,
                            "date_time":appointment.date_time,
                            "status": appointment.status }
            info.append(app_data)
    return info

@router.put("/adminUpdateAppointment/{id}")
def admin_update_appointment(id:int, data: AdminAppointmentUpdate,
                             db: Session = Depends(get_db),
                             current_admin: User = Depends(get_current_admin)):
    appointment = db.query(Appointment).filter(Appointment.appointment_id == id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment Not Found")
    
    if data.patient_name:
        patient_id = get_patient_id_by_Name(data.patient_name,db)
        if not Is_User_Valid(patient_id, "patient", db):
            raise HTTPException(status_code=404, detail="Patient Not Found")
        appointment.patient_id = patient_id
    
    #in case user didn't provide the new patient_name and the old patient status is no more valid
    if not Is_User_Valid(appointment.patient_id, "patient", db):
        raise HTTPException(status_code=404, detail="Patient Not Found")

    
    if data.doctor_name:
        doctor_id = get_doctor_id_by_Name(data.doctor_name,db)
        if not Is_User_Valid(doctor_id, "doctor", db):
            raise HTTPException(status_code=404, detail="Doctor Not Found") 
        appointment.doctor_id = doctor_id
        
    #in case user didn't provide the new doctor_name and the old doctor status is no more valid 
    if not Is_User_Valid(appointment.doctor_id, "doctor", db):
        raise HTTPException(status_code=404, detail="Doctor Not Found") 

    if data.description:
        appointment.description = data.description
    if data.date_time:
        appointment.date_time = data.date_time
    if data.status:
        if data.status.upper() not in allowed_status:
            raise HTTPException(status_code=404, detail="Invalid Appointment Status")
        appointment.status = data.status.upper()
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment Successfully Updated"}

@router.put("/userUpdateAppointment/{id}")
def user_update_appointment(id:int, data: UserAppointmentUpdate,
                             db: Session = Depends(get_db),
                             current_user: User = Depends(get_current_user)
                             ):
    appointment = db.query(Appointment).filter(Appointment.appointment_id == id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment Not Found")
    
    # Ensure that the logged-in user is a doctor/ patient and they are updating their own information
    if current_user.role == "doctor":
        doctor_id = isDoctorValid(current_user.user_id, db)
        if doctor_id == 0:
            raise HTTPException(status_code=404, detail="Doctor Privileges are Required")
        if appointment.doctor_id != doctor_id:
            raise HTTPException(status_code=404, detail="You Are Not Allowed to Update This Appointment")
        
    elif current_user.role == "patient":
        patient_id = isPatientValid(current_user.user_id, db)
        if patient_id == 0:
            raise HTTPException(status_code=404, detail="Patient Privileges are Required")
        if appointment.patient_id != patient_id:
            raise HTTPException(status_code=404, detail="You Are Not Allowed to Update This Appointment")
    

    if data.description:
        appointment.description = data.description
    if data.date_time:
        appointment.date_time = data.date_time
    if data.status:
        if data.status.upper() not in allowed_status:
            raise HTTPException(status_code=404, detail="Invalid Appointment Status")
        appointment.status = data.status.upper()
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment Successfully Updated"}

def get_user_appointments_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user_db =  db.query(User).filter(User.user_id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User Not Found")
    if user_db.role == "patient":
        id = get_patient_id_by_user_id(user_id,db)
        appointments = db.query(Appointment).filter(Appointment.patient_id == id).all()
    elif user_db.role == "doctor":
        id = get_doctor_id_by_user_id(user_id,db)
        appointments = db.query(Appointment).filter(Appointment.doctor_id == id).all()
    return appointments

@router.delete("/deactivateAppointment/{id}")
def deactivate_appointment(appointment_id:int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment Not Found")
    appointment.status = "CANCELLED"
    db.commit()
    db.refresh(appointment)
    return {"message": "Appointment Deactivated"}