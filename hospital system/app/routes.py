from flask import Flask,render_template,Blueprint,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from flask_mail import Mail
import json
from .forms import SignupForm, LoginForm, DoctorForm, PatientForm
from .models import User, Test, Patients, Doctors, Trigr
import os
import requests
import base64
import json
from flask import Blueprint, current_app, render_template, url_for, flash, redirect, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse
from .extensions import db
from.extensions import bcrypt

bp = Blueprint('main', __name__)



# here we will pass endpoints and run the fuction
@bp.route('/')
def index():
    return render_template('index.html')
    

@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, usertype=form.usertype.data, email=form.email.data)
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('signup.html', title='Signup', form=form)



@bp.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@bp.route('/doctors', methods=['POST', 'GET'])
def doctors():
    form = DoctorForm()
    if form.validate_on_submit():
        doctors_booking=DoctorForm(
            email=form.email.data, doctorname=form.doctorname.data, dept=form.dept.data
        )
        db.session.add(doctors_booking)
        db.session.commit()
        flash("Information is Stored", "primary")
    
    return render_template('doctor.html', form=form)


@bp.route('/patients', methods=['POST', 'GET'])
@login_required
def patients():
    doct = Doctors.query.all()
    form = PatientForm()
    form.dept.choices = [(doctor.dept, doctor.dept) for doctor in doct]
    
    if form.validate_on_submit():
        if len(form.number.data) != 10:
            flash("Please provide a 10-digit number", "warning")
            return render_template('patient.html', form=form, doct=doct)

        query = Patients(
            email=form.email.data,
            name=form.name.data,
            gender=form.gender.data,
            slot=form.slot.data,
            disease=form.disease.data,
            time=form.time.data,
            date=form.date.data,
            dept=form.dept.data,
            number=form.number.data
        )
        db.session.add(query)
        db.session.commit()
        flash("Booking Confirmed", "info")
    
    return render_template('patient.html', form=form, doct=doct)



@bp.route('/bookings')
@login_required
def bookings():
    posts = Doctors.query.filter_by(user_id=current_user.did).all()
    return render_template('booking.html', posts=posts)

    


@bp.route("/edit/<string:pid>",methods=['POST','GET'])
@login_required
def edit(email):    
    if request.method=="POST":
        pid=request.form.get("pid")
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        slot=request.form.get('slot')
        disease=request.form.get('disease')
        time=request.form.get('time')
        date=request.form.get('date')
        dept=request.form.get('dept')
        number=request.form.get('number')
        db.engine.execute(f"UPDATE `patients` SET `email` = '{email}', `name` = '{name}', `gender` = '{gender}', `slot` = '{slot}', `disease` = '{disease}', `time` = '{time}', `date` = '{date}', `dept` = '{dept}', `number` = '{number}' WHERE `patients`.`pid` = {pid}")
        post=Patients.query.filter_by(pid=pid).first()
        post.email=email
        post.name=name
        post.gender=gender
        post.slot=slot
        post.disease=disease
        post.time=time
        post.date=date
        post.dept=dept
        post.number=number
        db.session.commit()

        flash("Slot is Updates","success")
        return redirect('/bookings')
        
    posts=Patients.query.filter_by(email=email).first()
    return render_template('edit.html',posts=posts)


@bp.route("/delete/<string:pid>",methods=['POST','GET'])
@login_required
def delete(email):
    # db.engine.execute(f"DELETE FROM `patients` WHERE `patients`.`pid`={pid}")
    query=Patients.query.filter_by(pid=pid).first()
    db.session.delete(query)
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/bookings')








@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('main.login'))



@bp.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'
    

@bp.route('/details')
@login_required
def details():
    posts=Trigr.query.all()
    # posts=db.engine.execute("SELECT * FROM `trigr`")
    return render_template('trigers.html',posts=posts)


@bp.route('/search',methods=['POST','GET'])
@login_required
def search():
    if request.method=="POST":
        query=request.form.get('search')
        dept=Doctors.query.filter_by(dept=query).first()
        name=Doctors.query.filter_by(doctorname=query).first()
        if name:

            flash("Doctor is Available","info")
        else:

            flash("Doctor is Not Available","danger")
    return render_template('index.html')



