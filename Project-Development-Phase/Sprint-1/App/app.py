from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def register():
    return render_template('registration.html')

@app.route("/login")
def register():
    return render_template('login.html')

