
Debug     return super().validate(extra)
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/wtforms/form.py", line 146, in validate
    if not field.validate(self, extra):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/wtforms/fields/core.py", line 246, in validate
    stop_validation = self._run_validation_chain(form, chain)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/wtforms/fields/core.py", line 266, in _run_validation_chain
    validator(form, self)
  File "/home/harold/Desktop/Hospital-Management-System-dbmsminiproject-main/hospital system/app/forms.py", line 19, in validate_email
    user = User.query.filter_by(email=email.data).first()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/orm/query.py", line 2728, in first
    return self.limit(1)._iter().first()  # type: ignore
           ^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/orm/query.py", line 2827, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2362, in execute
    return self._execute_internal(
           ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/orm/session.py", line 2247, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/orm/context.py", line 293, in orm_execute_statement
    result = conn.execute(
             ^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1418, in execute
    return meth(
           ^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/sql/elements.py", line 515, in _execute_on_connection
    return connection._execute_clauseelement(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1640, in _execute_clauseelement
    ret = self._execute_context(
          ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1846, in _execute_context
    return self._exec_single_context(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1986, in _exec_single_context
    self._handle_dbapi_exception(
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 2355, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/base.py", line 1967, in _exec_single_context
    self.dialect.do_execute(
  File "/home/harold/my_flask_project/flask/lib/python3.12/site-packages/sqlalchemy/engine/default.py", line 941, in do_execute
    cursor.execute(statement, parameters)
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.username AS user_username, user.usertype AS user_usertype, user.email AS user_email, user.password AS user_password 
FROM user 
WHERE user.email = ?
 LIMIT ? OFFSET ?]
[parameters: ('joelharold@ymail.com', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
127.0.0.1 - - [19/Aug/2024 05:35:52] "POST /signup HTTP/1.1" 500 - for 




# app/models.py
from datetime import datetime
from .extensions import db, login_manager
from flask_login import UserMixin
from.extensions import bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# here we will create db models that is tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    usertype=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Patients(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    gender=db.Column(db.String(50))
    slot=db.Column(db.String(50))
    disease=db.Column(db.String(50))
    time=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(50),nullable=False)
    dept=db.Column(db.String(50))
    number=db.Column(db.String(50))

class Doctors(db.Model):
    did=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    doctorname=db.Column(db.String(50))
    dept=db.Column(db.String(50))

class Trigr(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    action=db.Column(db.String(50))
    timestamp=db.Column(db.String(50))

#init.py

from flask import Flask,render_template
from flask_cors import CORS
from flask_migrate import Migrate
import stripe
import paypalrestsdk
from .extensions import db, login_manager, bcrypt
from .routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    # Load configurations from config file
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    Migrate(app, db)
    # Register blueprints
    app.register_blueprint(main_bp)

    # Error handlers
    register_error_handlers(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback session to prevent issues on next DB call
        return render_template('500.html'), 500


# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import paypalrestsdk




db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()




#form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from .models import User
from wtforms.fields import TimeField
from wtforms import StringField, PasswordField, IntegerField, SubmitField,BooleanField,FloatField, SelectField, DecimalField,DateField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    usertype = SelectField('User Type', choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DoctorForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    doctorname = StringField('Doctor Name', validators=[DataRequired()])
    dept = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Add Doctor')

class PatientForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    slot = StringField('Slot', validators=[DataRequired()])
    disease = StringField('Disease', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()], format='%H:%M')
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    dept = StringField('Department', validators=[DataRequired()])
    number = StringField('Contact Number', validators=[DataRequired()])


    submit = SubmitField('Book Appointment')


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
        query = Doctors(email=form.email.data, doctorname=form.doctorname.data, dept=form.dept.data)
        db.session.add(query)
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
    em=current_user.email
    if current_user.usertype=="Doctor":
        # query=db.engine.execute(f"SELECT * FROM `patients`")
        query=Patients.query.all()
        return render_template('booking.html',query=query)
    else:
        # query=db.engine.execute(f"SELECT * FROM `patients` WHERE email='{em}'")
        query=Patients.query.filter_by(email=em)
        print(query)
        return render_template('booking.html',query=query)
    


@bp.route("/edit/<string:pid>",methods=['POST','GET'])
@login_required
def edit(pid):    
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        slot=request.form.get('slot')
        disease=request.form.get('disease')
        time=request.form.get('time')
        date=request.form.get('date')
        dept=request.form.get('dept')
        number=request.form.get('number')
        # db.engine.execute(f"UPDATE `patients` SET `email` = '{email}', `name` = '{name}', `gender` = '{gender}', `slot` = '{slot}', `disease` = '{disease}', `time` = '{time}', `date` = '{date}', `dept` = '{dept}', `number` = '{number}' WHERE `patients`.`pid` = {pid}")
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
        
    posts=Patients.query.filter_by(pid=pid).first()
    return render_template('edit.html',posts=posts)


@bp.route("/delete/<string:pid>",methods=['POST','GET'])
@login_required
def delete(pid):
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
    return redirect(url_for('login'))



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



