from sqlalchemy import Column, Integer, String, Boolean,DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Doctor(Base):
    __tablename__ = "doctor"
    doctor_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    doctor_specialty = Column(String, index=True, default = "General")
    is_doctor = Column(Boolean, index=True, default = True) 
    status_expiry = Column (DateTime)
    
    user = relationship("User", backref="doctor")
    appointment = relationship("Appointment", back_populates="doctor") 