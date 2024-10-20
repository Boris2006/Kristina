from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Таблица "Специализации врачей"
class DoctorSpecialization(db.Model):
    __tablename__ = 'doctor_specializations'
    specialization_id = db.Column(db.Integer, primary_key=True)
    specialization_name = db.Column(db.String(100), nullable=False)

# Таблица "Врачи"
class Doctor(db.Model):
    __tablename__ = 'doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    specialization_id = db.Column(db.Integer, db.ForeignKey('doctor_specializations.specialization_id'))
    specialization = db.relationship('DoctorSpecialization', backref='doctors')

# Таблица "Пациенты"
class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    patronymic = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)

# Таблица "Карточки пациентов"
class PatientCard(db.Model):
    __tablename__ = 'patient_cards'
    card_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    phone_number = db.Column(db.String(15), nullable=False)
    policy_number = db.Column(db.String(20), nullable=False)
    place_of_residence = db.Column(db.String(100), nullable=False)
    attending_physician_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    attending_physician = db.relationship('Doctor', backref='patient_cards')
    patient = db.relationship('Patient', backref='cards')

# Таблица "Визиты"
class Visit(db.Model):
    __tablename__ = 'visits'
    visit_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    visit_datetime = db.Column(db.DateTime, nullable=False)
    patient = db.relationship('Patient', backref='visits')
    doctor = db.relationship('Doctor', backref='visits')

