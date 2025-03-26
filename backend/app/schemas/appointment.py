from pydantic import BaseModel
from datetime import datetime

# pydantic model for appointment
class AppointmentCreate(BaseModel):
    patient_id : int
    doctor_id : int
    description : str
    date_time : datetime
    
class AppointmentUpdate(BaseModel):
    patient_id : int
    doctor_id : int
    description : str
    date_time : datetime
    status : str