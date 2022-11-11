from flask import Flask, render_template, url_for, flash, redirect, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mail import Mail, Message
import os
import cv2
import operator
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

class ChangePasswordForm(Form):
    new_password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('new_confirm', message='Passwords do not match')
    ])
    new_confirm = PasswordField('Confirm Password')
    

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/landingpage')
def landingpage():
    return render_template('landingpage.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/changepass', methods=["GET", "POST"])
def changepass():

    form = ChangePasswordForm(request.form)
    if request.method == "POST" and form.validate():
        form_password = form.new_password.data
        res = database.update_password(session['email'], form_password)
        flash('Your password has been changed successfully!', 'success')

    return render_template('change_password.html', form=form)

@app.route('/predict', methods=["GET", "POST"])
def predict():

    if request.method == "POST":
        
        if request.form.get("video") is None:
            error = "Please enable camera access!"
            return render_template('prediction.html', error=error)

        if  request.files["userfile"].filename == "":
            error = "Please upload an image!"
            return render_template('prediction.html', error=error)


        file = request.files['userfile']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath,'uploads',secure_filename(file.filename))
        file.save(file_path)
        print('Image saved successfully!')
        image1 = cv2.imread(file_path)

        if request.form.get("video") is not None:
            cap = cv2.VideoCapture(0)
            while True:
                _, frame = cap.read() 
                frame = cv2.flip(frame, 1)
                
                x1 = int(0.5*frame.shape[1]) 
                y1 = 10
                x2 = frame.shape[1]-10
                y2 = int(0.5*frame.shape[1])

                cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)
                roi = frame[y1:y2, x1:x2]
                
                roi = cv2.resize(roi, (64, 64)) 
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                _, test_image = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY)
                cv2.imshow("test", test_image)

                result = model.predict(test_image.reshape(1, 64, 64, 1))

                prediction = {'Zero': result[0][0], 
                            'One': result[0][1], 
                            'Two': result[0][2],
                            'Three': result[0][3],
                            'Four': result[0][4],
                            'Five': result[0][5]}

                prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
                
                cv2.putText(frame, prediction[0][0], (10, 120), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)    
                cv2.imshow("Frame", frame)
                
                image1=cv2.imread(file_path)
                
                if prediction[0][0]=='Zero':
                    
                    cv2.rectangle(image1, (480, 170), (650, 420), (0, 0, 255), 2)
                    cv2.imshow("Rectangle", image1)
                    key=cv2.waitKey(3000)
                    if (key & 0xFF) == ord("0"):
                        cv2.destroyWindow("Gesture 0 - Fixed Rectangle Drawing")

                elif prediction[0][0]=='One':
                
                    resized = cv2.resize(image1, (200, 200))
                    cv2.imshow("Gesture 1 - Fixed Resizing I(200,200)", resized)
                    key=cv2.waitKey(3000)
                    if (key & 0xFF) == ord("1"):
                        cv2.destroyWindow("Gesture 1 - Fixed Resizing I(200,200)")

                    
                elif prediction[0][0]=='Two':
                    (h, w, d) = image1.shape
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, -45, 1.0)
                    rotated = cv2.warpAffine(image1, M, (w, h))
                    cv2.imshow("Gesture 2 - OpenCV Rotation", rotated)
                    key=cv2.waitKey(3000)
                    if (key & 0xFF) == ord("2"):
                        cv2.destroyWindow("Gesture 2 - OpenCV Rotation")
                    
                elif prediction[0][0]=='Three':
                    blurred = cv2.GaussianBlur(image1, (21, 21), 0)
                    cv2.imshow("Gesture 3 - Blurring", blurred)
                    key=cv2.waitKey(3000)
                    if (key & 0xFF) == ord("3"):
                        cv2.destroyWindow("Gesture 3 - Blurring")

                elif prediction[0][0]=='Four':
                
                    resized = cv2.resize(image1, (400, 400))
                    cv2.imshow("Gesture 4 - Fixed Resizing II(400,400)", resized)
                    key=cv2.waitKey(3000)
                    if (key & 0xFF) == ord("4"):
                        cv2.destroyWindow("Gesture 4 - Fixed Resizing II(400,400)")

                elif prediction[0][0]=='Five':
                    gray = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
                    cv2.imshow("Gesture 5 - Grayscaling", gray)
                    key=cv2.waitKey(3000)
                    if (key & 0xFF) == ord("5"):
                        cv2.destroyWindow("Gesture 5 - Grayscaling")

                interrupt = cv2.waitKey(10)
                if interrupt & 0xFF == 27: # esc key
                    break
                   
            cap.release()
            cv2.destroyAllWindows()                

    return render_template('prediction.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        form_name = form.name.data
        form_email = form.email.data
        form_username = form.username.data
        form_password = form.password.data

        email_check = database.check_email_exists(form_email)
        if email_check == True:
            error = 'The email you entered already exists in the database!'
            return render_template('registration.html', error=error, form=form)
        
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
            session['email'] = email
            session['name'] = result_set['name']
            session['username'] = result_set['username']    
            session['number_of_access'] = len(user_sessions)
            session['last'] =  user_sessions[-1]
            
            return redirect(url_for('landingpage'))
             

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