from typing import List
import datetime as _dt
import pydantic as _pydantic


class _MedicineBase(_pydantic.BaseModel):
    name: str
    quantity: int
    time_for_medicine: str
    type: str
    start_date: _dt.date
    end_date: _dt.date


class MedicineCreate(_MedicineBase):
    pass


class Medicine(_MedicineBase):
    id: int
    patient_id: int
    created_at: _dt.datetime
    updated_at: _dt.datetime

    class Config:
        orm_mode = True


class _PatientBase(_pydantic.BaseModel):
    name: str
    phone: str
    address: str


class PatientCreate(_PatientBase):
    pass


class Patient(_PatientBase):
    id: int
    medicines: List[Medicine] = []

    class Config:
        orm_mode = True


# class MedicineWithPatient(_MedicineBase):
#     owner: List[Patient] = []

#     class Config:
#         orm_mode = True


class MedicinePatient(Medicine):
    patient: List[Patient] = []


class AssignMedicine(_pydantic.BaseModel):
    medicine: int
    patient: int


class MedicineID(_pydantic.BaseModel):
    id: List[int]
