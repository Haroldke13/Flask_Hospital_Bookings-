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
