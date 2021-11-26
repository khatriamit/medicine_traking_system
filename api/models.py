import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

# import database as _database
from api.database import Base

association_table = _sql.Table(
    "association",
    Base.metadata,
    _sql.Column("patients_id", _sql.ForeignKey("patients.id"), primary_key=True),
    _sql.Column("medicine_id", _sql.ForeignKey("medicine.id"), primary_key=True),
)


class Patient(Base):
    __tablename__ = "patients"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, unique=True, index=True)
    phone = _sql.Column(_sql.String, unique=True, index=True)
    address = _sql.Column(_sql.String)

    medicines = _orm.relationship(
        "Medicine",
        secondary=association_table,
        back_populates="patient",
    )


class Medicine(Base):
    __tablename__ = "medicine"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    time_for_medicine = _sql.Column(_sql.String)
    patient_id = _sql.Column(_sql.Integer, _sql.ForeignKey("patients.id"))
    start_date = _sql.Column(_sql.Date)
    end_date = _sql.Column(_sql.Date)
    quantity = _sql.Column(_sql.Integer)
    type = _sql.Column(_sql.String)
    created_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    updated_at = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    patient = _orm.relationship(
        "Patient",
        secondary=association_table,
        back_populates="medicines",
    )
