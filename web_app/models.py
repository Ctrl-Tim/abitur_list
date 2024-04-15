from web_app import db, manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    patronymic = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telephone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(500), nullable=True)

class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, unique=True)
    site_link = db.Column(db.String(500), nullable=True, unique=True)

    specialties = db.relationship('Specialty', back_populates='faculty')

class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    profile = db.Column(db.String(500))
    number = db.Column(db.String(15), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    faculty = db.relationship('Faculty', back_populates='specialties')

class IndividualAchievements(db.Model):
    __tablename__ = 'individualachievementss'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Applicant(db.Model):
    __tablename__ = 'applicants'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(500), nullable=False)
    ege1 = db.Column(db.Integer, nullable=False)
    ege2 = db.Column(db.Integer, nullable=False)
    ege3 = db.Column(db.Integer, nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'), nullable=False)
    individualachievements1_id = db.mapped_column(db.Integer, db.ForeignKey('individualachievementss.id'), nullable=True)
    individualachievements2_id = db.mapped_column(db.Integer, db.ForeignKey('individualachievementss.id'), nullable=True)
    specialty = db.relationship('Specialty')
    individualachievements1 = db.relationship('IndividualAchievements', foreign_keys=[individualachievements1_id])
    individualachievements2 = db.relationship('IndividualAchievements', foreign_keys=[individualachievements2_id])



@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)