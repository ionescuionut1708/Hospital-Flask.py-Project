from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy_utils import database_exists, create_database
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'REEGW(!@#@*FDS*DC<>SDAIQ*E@#FESDW#@$34225125574'  # cheie secretă pentru JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'  # Configurează URI-ul bazei de date
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Modele de date
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Adaugă alte câmpuri relevante pentru doctor

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Adaugă alte câmpuri relevante pentru pacient

class Assistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Adaugă alte câmpuri relevante pentru asistent

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    # Adaugă alte câmpuri relevante pentru tratament

# Decorator pentru roluri
def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if 'role' not in current_user or current_user['role'] != role:
                return jsonify({'message': 'Unauthorized access'}), 401
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Ruta pentru register
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    role = request.json.get('role', None)

    if not username or not password or not role:
        return jsonify({'message': 'Missing fields'}), 400

    if role not in ['General Manager', 'Doctor', 'Assistant']:
        return jsonify({'message': 'Invalid role'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Ruta pentru autentificare
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity={'username': username, 'role': user.role})
        return jsonify({'access_token': access_token, 'role': user.role}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Rute pentru doctori
@app.route('/doctors', methods=['GET'])
@jwt_required()
@role_required('General Manager')
def get_doctors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    doctors = Doctor.query.paginate(page=page, per_page=per_page)
    return jsonify([{'id': doctor.id, 'name': doctor.name} for doctor in doctors.items]), 200

@app.route('/doctors', methods=['POST'])
@jwt_required()
@role_required('General Manager')
def add_doctor():
    name = request.json.get('name', None)
    if not name:
        return jsonify({'message': 'Missing fields'}), 400
    doctor = Doctor(name=name)
    db.session.add(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor added successfully'}), 201

# Rute pentru pacienți
@app.route('/patients', methods=['GET'])
@jwt_required()
@role_required('Doctor')
def get_patients():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    patients = Patient.query.paginate(page=page, per_page=per_page)
    return jsonify([{'id': patient.id, 'name': patient.name} for patient in patients.items]), 200

@app.route('/patients', methods=['POST'])
@jwt_required()
@role_required('Doctor')
def add_patient():
    name = request.json.get('name', None)
    if not name:
        return jsonify({'message': 'Missing fields'}), 400
    patient = Patient(name=name)
    db.session.add(patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully'}), 201

# Rute pentru asistenți
@app.route('/assistants', methods=['GET'])
@jwt_required()
@role_required('General Manager')
def get_assistants():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    assistants = Assistant.query.paginate(page=page, per_page=per_page)
    return jsonify([{'id': assistant.id, 'name': assistant.name} for assistant in assistants.items]), 200

# Rute pentru tratamente
@app.route('/treatments', methods=['GET'])
@jwt_required()
@role_required('Doctor')
def get_treatments():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    treatments = Treatment.query.paginate(page=page, per_page=per_page)
    return jsonify([{'id': treatment.id, 'description': treatment.description} for treatment in treatments.items]), 200

@app.route('/treatments', methods=['POST'])
@jwt_required()
@role_required('Doctor')
def add_treatment():
    description = request.json.get('description', None)
    if not description:
        return jsonify({'message': 'Missing fields'}), 400
    treatment = Treatment(description=description)
    db.session.add(treatment)
    db.session.commit()
    return jsonify({'message': 'Treatment added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        # Verifică dacă baza de date există și are tabelele necesare
        if not database_exists(db.engine.url):
            db.create_all()
        else:
            inspector = inspect(db.engine)
            if not inspector.has_table('user'):
                db.create_all()
    app.run(debug = True, port = 5000)