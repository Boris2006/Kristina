from flask import Flask, request, jsonify, render_template
from models import db, Doctor, Patient, PatientCard, Visit, DoctorSpecialization
from config import Config
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)



db.init_app(app)

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# CRUD операции для Doctor

@app.route('/doctors')
def doctors():
    all_doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=all_doctors)

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        specialization_id = request.form['specialization']  # Изменяем на specialization_id

        # Добавляем врача в базу данных
        new_doctor = Doctor(first_name=first_name, last_name=last_name, specialization_id=specialization_id)
        db.session.add(new_doctor)
        db.session.commit()

        return redirect('/doctors')  # Перенаправляем на страницу со списком врачей после добавления

    # Если GET-запрос, то возвращаем HTML-форму
    return render_template('add_doctor.html')


@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{
        'doctor_id': doctor.doctor_id,
        'first_name': doctor.first_name,
        'last_name': doctor.last_name,
        'specialization_id': doctor.specialization_id
    } for doctor in doctors])

# Аналогичные CRUD маршруты для других сущностей (пациентов, визитов, карточек)

@app.route('/patients.html')
def patients():
    all_patients = Patient.query.all()
    return render_template('patients.html', patients=all_patients)

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender'][0]
        dob = request.form['dob']  # формат даты 'YYYY-MM-DD'
        
        new_patient = Patient(first_name=first_name, last_name=last_name, gender=gender, date_of_birth=dob)
        db.session.add(new_patient)
        db.session.commit()
        return redirect('/patients')
    return render_template('add_patient.html')




from datetime import datetime

@app.route('/add_visit', methods=['GET', 'POST'])
def add_visit():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        visit_date_str = request.form['visit_date']  # Получаем дату как строку
        # Преобразуем строку в объект datetime
        visit_datetime = datetime.strptime(visit_date_str, '%Y-%m-%d')

        # Создаем новый объект Visit
        new_visit = Visit(patient_id=patient_id, doctor_id=doctor_id, visit_datetime=visit_datetime)
        db.session.add(new_visit)
        db.session.commit()
        return redirect('/visits')
    
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('add_visit.html', patients=patients, doctors=doctors)


@app.route('/visits')
def visits():
    all_visits = Visit.query.all()
    return render_template('visits.html', visits=all_visits)

@app.route('/delete_visit/<int:id>')
def delete_visit(id):
    visit = Visit.query.get_or_404(id)
    db.session.delete(visit)
    db.session.commit()
    return redirect('/visits')



@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect('/doctors')

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    patient = Patient.query.filter_by(patient_id=id).first_or_404()
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patients'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
