from flask import Flask, render_template, url_for, flash, redirect, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mail import Mail, Message
import os
import cv2
from time import sleep
import numpy as np
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from datetime import datetime
import database

app = Flask(__name__)
mail = Mail(app)
model = load_model('../Model/gesture.h5')
print("Model Loaded!")

results = {0: "Zero", 1: "One", 2: "Two", 3:"Three", 4:"Four", 5: "Five"}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'XXX'
app.config['MAIL_PASSWORD'] = 'XXX'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

def model_predict(file_path):
        input_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        input_image = cv2.resize(input_image, (64,64))
        #print(input_image, input_image.shape)
        predictions = model.predict(input_image.reshape(1,64,64,1))
        return predictions


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/landing')
def landingpage():
    return render_template('landingpage.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/predict', methods=["GET", "POST"])
def predict():

    if request.method == "POST":
        #print("Video vals: ", request.form.get("video"))
        
        if request.form.get("video") is not None:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break  
            cap.release()
            cv2.destroyAllWindows()
        
        else:
            file = request.files['userfile']
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(basepath,'uploads',secure_filename(file.filename))
            file.save(file_path)
            print('Image saved successfully!')

            predictions = model_predict(file_path)
            print(predictions)
            session['prediction'] = results[np.argmax(predictions)]

    return render_template('prediction.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        form_name = form.name.data
        form_email = form.email.data
        form_username = form.username.data
        form_password = form.password.data

        res = database.users_insert(form_name, form_username, form_email, form_password)

        flash('You are now registered and can login!', 'success')
        msg = Message('Registration Verfication', sender="anirudh19015@cse.ssn.edu.in", recipients=[form_email])
        msg.body = (f'Congratulations! Welcome user! Your Credentials are Username: {form_username} Password: {form_password}')
        mail.send(msg)
        print("Email Sent!")

    return render_template('registration.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        candidate_password = request.form["password"]
        #print("Email is", email)
        result_set = database.users_fetch_by_email(email)

        if type(result_set) != type(False):
            if result_set['password'] != candidate_password:
                error = 'Invalid login!'
                return render_template('login.html', error=error)
            
            database.usession_insert(email)
            user_sessions = database.usession_fetch_by_email(email)
            print(user_sessions)

            session['logged_in'] = True
            session['name'] = result_set['name']
            session['username'] = result_set['username']    
            session['number_of_access'] = len(user_sessions)
            session['last'] =  user_sessions[-1]
            
            return render_template('landingpage.html')
             

        else:
            error = 'User not found! Please enter the correct username and/or password.'
            return render_template('login.html', error=error)
    
    return render_template('login.html')
        
@app.route('/signout')
def signout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key="secret123"
    app.run(debug=True)