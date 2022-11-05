from flask import Flask, render_template, url_for, flash, redirect, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        return render_template('registration.html', form=form) #change    
    
    elif request.method == "GET":
        return render_template('registration.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return render_template('login.html') #change
    
    elif request.method == "GET":
        return render_template('login.html')
        
if __name__ == "__main__":
    app.run(debug=True)