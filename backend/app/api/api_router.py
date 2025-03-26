from fastapi import APIRouter
from api.endpoints import auth, patients, admin, doctors, appointments

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
# api_router.include_router(appointments.router, prefix="/appointment", tags=["Appointments"])