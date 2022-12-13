from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,DateField,RadioField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from brokerapp.models import User
from flask_wtf.file import FileField,FileAllowed




class Registration(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=40)],render_kw={"placeholder": "Username"})
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder": "Email"})
    password=PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder": "Password"})
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    firstname=StringField("First Name",validators=[DataRequired(),Length(min=2,max=40)],render_kw={"placeholder": "First Name"})
    lastname=StringField("Last Name",validators=[DataRequired(),Length(min=2,max=40)],render_kw={"placeholder": "Last Name"})
    dob=DateField("DOB",validators=[DataRequired()])
    category=RadioField("Category",choices=["Male","Female","Others"])
    
    
    submit=SubmitField("Register")

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken . Please chosse other')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken')

class Login(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder": "Email"})
    password=PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder": "Password"})
    remember = BooleanField('Remeber Me', default=False)
    submit=SubmitField("Log In")

class Updateaccount(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=2,max=40)],render_kw={"placeholder": "Username"})
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder": "Email"})
    firstname=StringField("First Name",validators=[DataRequired(),Length(min=2,max=40)],render_kw={"placeholder": "First Name"})
    lastname=StringField("Last Name",validators=[DataRequired(),Length(min=2,max=40)],render_kw={"placeholder": "Last Name"})
    dob=DateField("DOB",validators=[DataRequired()])
    picture=FileField("Update Profile Picture",validators=[FileAllowed(["jpg","jpeg","png","jfif"])])
    submit=SubmitField("Update")

    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken . Please chosse other')
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken')


class RequestresetForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder": "Email for reseting Password"})
    submit=SubmitField("Request Reset Password Link")

    def verify_email(self,email):
        user=User.query.filter_by(email=email).first()
        if user is None:
            raise ValidationError("There is no account on this email {email}")


class ResetPasswordForm(FlaskForm):
    password=PasswordField("Password",validators=[DataRequired()],render_kw={"placeholder": "Password"})
    confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit=SubmitField("Reset Password")




