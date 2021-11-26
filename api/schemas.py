from typing import List
import datetime as _dt
import pydantic as _pydantic
import api.constants as _cons


class _MedicineBase(_pydantic.BaseModel):
    name: str
    quantity: int
    time_for_medicine: str
    type: _cons.MedicineTypes
    start_date: _dt.date
    end_date: _dt.date

    @_pydantic.root_validator
    def check_passwords_match(cls, values):
        start_date, end_date = values.get("start_date"), values.get("end_date")
        if start_date > end_date:
            raise ValueError("start date is ahead than end date")
        if start_date < _dt.date.today():
            raise ValueError("past date not allowed")
        return values


class MedicineCreate(_MedicineBase):
    pass


class Medicine(_MedicineBase):
    id: int
    # patient_id: int
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

    class Config:
        orm_mode = True


class Patient(_PatientBase):
    id: int
    medicines: List[Medicine] = []

    class Config:
        orm_mode = True


class MedicinePatient(Medicine):
    patient: List[PatientCreate] = []


class AssignMedicine(_pydantic.BaseModel):
    medicine: int
    patient: int


class MedicineID(_pydantic.BaseModel):
    id: List[int]


class MyMedicine(_pydantic.BaseModel):
    name: str
    quantity: int
    time_for_medicine: str
    type: _cons.MedicineTypes
    start_date: _dt.date
    end_date: _dt.date
