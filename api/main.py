from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import api.services as _services, api.schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/patients/", response_model=_schemas.Patient)
def create_patient(
    patient: _schemas.PatientCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_patient = _services.get_patient_by_name(
        db=db, name=patient.name, phone=patient.phone
    )
    if db_patient:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_patient(db=db, patient=patient)


@app.get("/patients/", response_model=List[_schemas.PatientCreate])
def read_patients(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    patients = _services.get_patients(db=db, skip=skip, limit=limit)
    return patients


@app.get("/patients/{patient_id}", response_model=_schemas.Patient)
def read_patient(
    patient_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_patient = _services.get_patient(db=db, patient_id=patient_id)
    if db_patient is None:
        raise _fastapi.HTTPException(
            status_code=404,
            detail="sorry this patient does not exist",
        )
    return db_patient


@app.post("/patients/{patient_id}/medicines/", response_model=_schemas.MedicinePatient)
def create_medicine(
    patient_id: int,
    medicine: _schemas.MedicineCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_patient(db=db, patient_id=patient_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return _services.create_medicine(db=db, medicine=medicine, patient_id=patient_id)


@app.get("/medicines/", response_model=List[_schemas.Medicine])
def get_medicines(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    medicines = _services.get_medicines(db=db, skip=skip, limit=limit)
    return medicines


@app.get("/medicines/{medicine_id}", response_model=_schemas.MedicinePatient)
def get_medicine(
    medicine_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    medicine = _services.get_medicine(db=db, medicine_id=medicine_id)
    if medicine is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this medicine does not exist"
        )

    return medicine


@app.delete("/medicines/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    _services.delete_medicine(db=db, medicine_id=medicine_id)
    return {"message": f"successfully deleted medicine with id: {medicine_id}"}


@app.put("/medicines/{medicine_id}", response_model=_schemas.Medicine)
def update_medicine(
    medicine_id: int,
    medicine: _schemas.MedicineCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.update_medicine(
        db=db,
        medicine=medicine,
        medicine_id=medicine_id,
    )


@app.post("/patient/{patient_id}/mark_taken/")
def mark_taken(
    medicine_ids: _schemas.MedicineID,
    patient_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    id_list = medicine_ids.dict().get("id")
    _services.mark_taken(db, id_list, patient_id)


@app.post("/assige_medicine/", response_model=_schemas.MedicinePatient)
def assign_medicine(
    assign: _schemas.AssignMedicine,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.assing_medicine(db, assign)
