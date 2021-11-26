from typing import List
from fastapi.encoders import jsonable_encoder
import sqlalchemy.orm as _orm
import fastapi as _fastapi


import api.models as _models, api.schemas as _schemas, api.database as _database


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_patient(db: _orm.Session, patient_id: int):
    return db.query(_models.Patient).filter(_models.Patient.id == patient_id).first()


def get_patient_by_name(db: _orm.Session, name: str, phone: str):
    return db.query(_models.Patient).filter(_models.Patient.name == name).first()


def get_patients(db: _orm.Session, skip: int = 0, limit: int = 100):
    query = db.query(_models.Patient).offset(skip).limit(limit).all()
    return jsonable_encoder(query)


def create_patient(db: _orm.Session, patient: _schemas.PatientCreate):
    db_patient = _models.Patient(
        name=patient.name,
        phone=patient.phone,
        address=patient.address,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_medicines(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Medicine).offset(skip).limit(limit).all()


def create_medicine(
    db: _orm.Session, medicine: _schemas.MedicineCreate, patient_id: int
):
    medicine = _models.Medicine(**medicine.dict(), patient_id=patient_id)
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine


def get_medicine(db: _orm.Session, medicine_id: int):
    return db.query(_models.Medicine).filter(_models.Medicine.id == medicine_id).first()


def delete_medicine(db: _orm.Session, medicine_id: int):
    db.query(_models.Medicine).filter(_models.Medicine.id == medicine_id).delete()
    db.commit()


def update_medicine(
    db: _orm.Session,
    medicine_id: int,
    medicine: _schemas.MedicineCreate,
):
    db_medicine = get_medicine(db=db, medicine_id=medicine_id)
    db_medicine.name = medicine.name
    db_medicine.type = medicine.type
    db_medicine.time_for_medicine = medicine.time_for_medicine
    db_medicine.start_date = medicine.start_date
    db_medicine.end_date = medicine.end_date
    db_medicine.quantity = medicine.quantity
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


def get_patient_medicine(db: _orm.Session, patient_id: int):
    db_patient = (
        db.query(_models.Patient).filter(_models.Patient.id == patient_id).first()
    )
    meds = db_patient.medicines
    my_meds = []
    for med in meds:
        my_meds.append(med.id)
    return my_meds


def substract_quantity(db: _orm.Session, ids: List):
    for medicine_id in ids:
        db_medicine = get_medicine(db=db, medicine_id=medicine_id)
        if db_medicine.quantity > 1:
            db_medicine.quantity -= 1
            db.commit()
            db.refresh(db_medicine)
        else:
            raise _fastapi.HTTPException(
                status_code=400,
                detail=f"your medicine {medicine_id} has already been completed",
            )


def mark_taken(db: _orm.Session, id: List, patient_id: int):
    my_meds = get_patient_medicine(db, patient_id=patient_id)
    for i in id:
        if i not in my_meds:
            raise _fastapi.HTTPException(
                status_code=400,
                detail=f"sorry medicine {i} does not exist in your meds",
            )
    substract_quantity(db, ids=id)


def assing_medicine(db: _orm.Session, assign: _schemas.AssignMedicine):
    db_medicine = (
        db.query(_models.Medicine)
        .filter(_models.Medicine.id == assign.medicine)
        .first()
    )
    db_patient = (
        db.query(_models.Patient).filter(_models.Patient.id == assign.patient).first()
    )

    db_medicine.patient.append(db_patient)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine
