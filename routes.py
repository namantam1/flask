from flask import Flask,render_template,url_for,redirect,flash,request,abort
from .models import User
from .form import LoginForm, RegistrationForm
from . import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
import secrets,os

@app.route("/home")
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login succesfully! you can now make posts here","success")
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Invalid username, password! Please check and fill again.","danger")
    return render_template('login.html',form = form,tagline="login")

@app.route("/signup",methods=['POST','GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypt_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(name=form.name.data,username=form.username.data,email=form.email.data,password=encrypt_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created successfully for {form.username.data}!",'success')
        return redirect(url_for('login'))
    return render_template('signup.html',form = form,tagline="signup")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))