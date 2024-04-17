import flask_login
from flask import Flask, render_template, redirect, url_for, request, flash, g
from web_app import app, db
from web_app.models import User, Faculty, Specialty, IndividualAchievements, Applicant
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath





"""""""""""
ГЛАВНАЯ
"""""""""""
@app.route('/', methods=['GET'])
def home():
    faculties = Faculty.query.all()
    return render_template('home.html', faculties=faculties)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response



"""""""""""""""
ПОЛЬЗОВАТЕЛИ
"""""""""""""""
@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(email=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Неверный логин или пароль!")
    return render_template('auth.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/users', methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
@login_required
def user_add():
    lastname = request.form.get('lastname')
    surname = request.form.get('surname')
    patronymic = request.form.get('patronymic')
    email = request.form.get('email')
    telephone = request.form.get('telephone')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    image_path = "img/users/default_avatar.jpg"

    errors = False

    if request.method == 'POST':
        if User.query.filter_by(email=email).first():
            errors = True
            flash("Данная почта уже занята другим пользователем!")

        if User.query.filter_by(telephone=telephone).first():
            errors = True
            flash("Данный номер уже занят другим пользователем!")

        if password != password2:
            errors = True
            flash("Пароли не совпадают!")

        if errors:
            return render_template('user_add.html', lastname=lastname, surname=surname, patronymic=patronymic,
                                   email=email, telephone=telephone)
        else:
            if 'avatar' in request.files:
                image_file = request.files['avatar']
                if image_file.filename != '':
                    outputimage, format = image_file.filename.split('.')
                    filename = "avatar (" + lastname + " " + surname + " " + patronymic + ")." + format
                    image_file.save(os.path.join(join(dirname(realpath(__file__)), "static/img/users"), filename))
                    image_path = "img/users/" + filename

            hash_pwd = generate_password_hash(password)
            new_user = User(lastname=lastname, surname=surname, patronymic=patronymic,
                            email=email, telephone=telephone, image_path=image_path, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('users'))

    return render_template('user_add.html')

@app.route('/users/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    if flask_login.current_user.id == 1 or flask_login.current_user.id == int(user_id):
        user = User.query.filter_by(id=user_id).first()

        lastname = request.form.get('lastname')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        new_password = request.form.get('new_password')
        new_password2 = request.form.get('new_password2')

        errors = False

        if request.method == 'POST':
            if User.query.filter_by(email=email).first() and user.email != email:
                errors = True
                flash("Данная почта уже занята другим пользователем!")

            if User.query.filter_by(telephone=telephone).first() and user.telephone != telephone:
                errors = True
                flash("Данный номер уже занят другим пользователем!")

            if len(new_password) > 4:
                if new_password != new_password2:
                    errors = True
                    flash("Пароли не совпадают!")

            if errors:
                return render_template('user_edit.html', lastname=user.lastname, surname=user.surname,
                                       patronymic=user.patronymic, email=user.email, telephone=user.telephone)
            else:
                if 'avatar' in request.files:
                    image_file = request.files['avatar']
                    if image_file.filename != '':
                        outputimage, format = image_file.filename.split('.')
                        filename = "avatar (" + lastname + " " + surname + " " + patronymic + ")." + format
                        image_file.save(os.path.join(join(dirname(realpath(__file__)), "static/img/users"), filename))
                        image_path = "img/users/" + filename
                        user.image_path = image_path

                if len(new_password) > 3:
                    hash_pwd = generate_password_hash(new_password)
                    user.password = hash_pwd

                if flask_login.current_user.id == 1:
                    user.lastname = lastname
                    user.surname = surname
                    user.patronymic = patronymic
                user.email = email
                user.telephone = telephone

                db.session.commit()

            return redirect(url_for('users'))

    return render_template('user_edit.html', lastname=user.lastname, surname=user.surname, patronymic=user.patronymic,
                                       email=user.email, telephone=user.telephone)

@app.route('/users/delete/<user_id>', methods=['GET', 'POST'])
@login_required
def user_delete(user_id):
    if flask_login.current_user.id == 1:
        User.query.filter_by(id=int(user_id)).delete()
        db.session.commit()
    return redirect(url_for('users'))



"""""""""""""""
СПРАВКИ
"""""""""""""""
@app.route('/faculties', methods=['GET'])
def faculties():
    faculties = Faculty.query.order_by(Faculty.name.asc()).all()
    return render_template('faculties.html', faculties=faculties)

@app.route('/individual_achievements', methods=['GET'])
def individual_achievements():
    individual_achievements = IndividualAchievements.query.all()
    return render_template('individual_achievements.html', individual_achievements=individual_achievements)



"""""""""""""""""""""
СПИСОК АБИТУРИЕНТОВ
"""""""""""""""""""""
@app.route('/applicants', methods=['GET', 'POST'])
def applicants():
    applicants = Applicant.query.all()
    return render_template('applicants.html', applicants=applicants)

@app.route('/applicants/add', methods=['GET', 'POST'])
def applicant_add():
    faculties = Faculty.query.all()
    specialties = Specialty.query.all()
    ia = IndividualAchievements.query.all()

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        faculty_id = int(request.form.get('faculties'))
        specialty_id = int(request.form.get('specialties'))
        ege1 = int(request.form.get('ege1'))
        ege2 = int(request.form.get('ege2'))
        ege3 = int(request.form.get('ege3'))
        individual1 = int(request.form.get('individual1'))
        individual2 = int(request.form.get('individual2'))

        errors = False

        if not Specialty.query.filter_by(id=specialty_id).first():
            errors = True
            flash("Выберите специальность!")

        if Applicant.query.filter_by(fullname=fullname, ege1=ege1, ege2=ege2, ege3=ege3, specialty_id=specialty_id).first():
            errors = True
            flash("Такая запись уже существует!")

        if errors:
            return render_template('applicant_add.html', faculties=faculties, specialties=specialties, ia=ia,
                                   fullname=fullname, ege1=ege1, ege2=ege2, ege3=ege3, individual1=individual1, individual2=individual2,
                                   faculty_id=faculty_id, specialty_id=specialty_id)

        new_applicant = Applicant(
            fullname=fullname,
            specialty_id=specialty_id,
            ege1=ege1,
            ege2=ege2,
            ege3=ege3)
        if individual1 != 0:
            new_applicant.individualachievements1_id = individual1
        if individual2 != 0:
            new_applicant.individualachievements2_id = individual2
        db.session.add(new_applicant)
        db.session.commit()

        return redirect(url_for('applicants'))

    return render_template('applicant_add.html', faculties=faculties, specialties=specialties, ia=ia)

@app.route('/applicants/<a_id>/edit', methods=['GET', 'POST'])
def applicant_edit(a_id):
    faculties = Faculty.query.all()
    specialties = Specialty.query.all()
    ia = IndividualAchievements.query.all()
    select_applicant = Applicant.query.filter_by(id=int(a_id)).first()

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        specialty_id = int(request.form.get('specialties'))
        ege1 = int(request.form.get('ege1'))
        ege2 = int(request.form.get('ege2'))
        ege3 = int(request.form.get('ege3'))
        individual1 = int(request.form.get('individual1'))
        individual2 = int(request.form.get('individual2'))

        errors = False

        if not Specialty.query.filter_by(id=specialty_id).first():
            errors = True
            flash("Выберите специальность!")

        check = Applicant.query.filter_by(fullname=fullname, ege1=ege1, ege2=ege2, ege3=ege3, specialty_id=specialty_id).first()
        if check.id != select_applicant.id:
            errors = True
            flash("Такая запись уже существует!")

        if errors:
            return redirect(url_for('applicant_edit', a_id=a_id))

        if individual1 != 0:
            select_applicant.individualachievements1_id = individual1
        else:
            select_applicant.individualachievements1_id = individual1
        if individual2 != 0:
            select_applicant.individualachievements2_id = individual2
        else:
            select_applicant.individualachievements2_id = individual2

        select_applicant.fullname = fullname
        select_applicant.specialty_id = specialty_id
        select_applicant.ege1 = ege1
        select_applicant.ege2 = ege2
        select_applicant.ege3 = ege3

        db.session.commit()

        return redirect(url_for('applicants'))

    return render_template('applicant_edit.html', faculties=faculties, specialties=specialties, ia=ia, applicant=select_applicant)

@app.route('/applicants/delete/<a_id>', methods=['GET', 'POST'])
@login_required
def applicant_delete(a_id):
    Applicant.query.filter_by(id=int(a_id)).delete()
    db.session.commit()
    return redirect(url_for('applicants'))