from flask import Flask, render_template, url_for, flash, redirect, session, logging, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import database

app = Flask(__name__)

@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/landing')
def landingpage():
    return render_template('landingpage.html')

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
        form_name = form.name.data
        form_email = form.email.data
        form_username = form.username.data
        form_password = form.password.data

        res = database.users_insert(form_name, form_username, form_email, form_password)

        flash('You are now registered and can login!', 'success')

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
            
            session['logged_in'] = True
            session['username'] = result_set['username']    
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