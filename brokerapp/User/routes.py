import os
from flask import Blueprint
users=Blueprint('users',__name__)

from flask import url_for,redirect,flash,render_template,request
from flask_login import current_user,login_required,logout_user,login_user
from brokerapp import db,bcrypt,createapp
from brokerapp.models import User
from brokerapp.User.models import send_email
from brokerapp.User.forms import Login,Registration,Updateaccount,RequestresetForm,ResetPasswordForm
from brokerapp.Utilities.models import save_image
app=createapp()

@users.route("/register",methods=['GET','POST'])
def register():
    form=Registration()
    if current_user.is_authenticated:
        return redirect(url_for('utilities.home'))
    if form.validate_on_submit():
        hase_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hase_pass,firstname=form.firstname.data,lastname=form.lastname.data,dob=form.dob.data,category=form.category.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {form.username.data}!")
        return redirect(url_for('users.login'))

    return render_template("register.html",title="register",form=form)

@users.route("/login",methods=['GET','POST'])
def login():
    form=Login()
    if current_user.is_authenticated:
        return redirect(url_for('utilities.home'))

    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next=request.args.get("next")
            return redirect(next) if next else redirect(url_for('utilities.home'))
        else:

            flash(f"Login unsuessfull for {form.email.data}! Please check email or password.")

    return render_template("login.html",title="Login-PostWorld",form=form)


@users.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    form=Updateaccount()
    image_add=url_for("static",filename="/images/"+current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            imgpath=save_image(form.picture.data)
            print(imgpath)
            try:
                if current_user.image_file !="Pro_default.jpg ":
                    os.remove(app.root_path+'/static/images/'+current_user.image_file) #delete existing picture
            except:
                pass
            current_user.image_file=imgpath
            db.session.commit()
        current_user.username=form.username.data
        current_user.email=form.email.data
        current_user.firstname=form.firstname.data
        current_user.lastname=form.lastname.data
        current_user.dob=form.dob.data


        db.session.commit()
        flash("Account details has been updated!")
        return redirect(url_for('utilities.home'))
    image_add=".."+image_add
    # # print(image_add)
    form.username.data=current_user.username
    form.email.data=current_user.email
    form.firstname.data=current_user.firstname
    form.lastname.data=current_user.lastname
    form.dob.data=current_user.dob

    return render_template('account.html',title="Account",image_file=image_add,form=form)

@users.route("/password/reset",methods=['GET','POST'])
def password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('utilities.home'))
    form=RequestresetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash("A email with containing password reset link has been send.")
            return redirect(url_for('users.login'))
        else:
            flash("No User Found")
        return render_template('resetpassword.html',title="Password Reset",form=form)
    return render_template('resetpassword.html',title="Password Reset",form=form)

@users.route("/resetpassword/<token>",methods=['GET','POST'])

def resetpassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('utilities.home'))
    user=User.verify_token(token)
    if user is None:
        flash("Invaild Token or Expired")
        return redirect(url_for('users.password_reset'))

    form=ResetPasswordForm()
    if form.validate_on_submit():
        hase_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hase_pass
        db.session.add(user)
        db.session.commit()
        flash(f"Password Changed for {user.email}!")
        return redirect(url_for('users.login'))

    return render_template("resetpasswordform.html",title="Reset Password",form=form,user_email=user.email)