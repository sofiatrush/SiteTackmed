from flask import Flask, request, session, jsonify, render_template, redirect, url_for, flash
import os
import hashlib
from database import DatabaseManager
import sqlite3

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = "supersecretkey" 

DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

db_manager = DatabaseManager(DATABASE)

@app.teardown_appcontext
def close_db(error):
    db_manager.close_db(error)


@app.route("/")
def home():
    pass

@app.route("/login", methods=["GET", "POST"])
def login():
    pass

@app.route("/register", methods=["GET", "POST"])
def register():
    pass

@app.route("/logout")
def logout():
    pass

@app.route("/theory")
def theory():
    pass

@app.route("/theory/Blood")
def Blood():
    pass

@app.route("/theory/BloodHelp")
def BloodHelp():
    pass

@app.route("/theory/ambulance")
def ambulance():
    pass

@app.route("/theory/march")
def march():
    pass

@app.route("/theory/burns")
def burns():
    pass

@app.route("/theory/consciousness")
def consciousness():
    pass

@app.route("/theory/examination")
def examination():
    pass

@app.route("/theory/frostbite")
def frostbite():
    pass

@app.route("/contacts")
def contacts():
    pass

@app.route("/profile")
def profile():
    pass

@app.route('/tests', methods=['GET'])
def tests_menu():
    pass

app.route('/test1')
def test1_page():
    pass

@app.route('/test2')
def test2_page():
    pass

@app.route('/submitTestResults', methods=['POST'])
def submit_test_results():
    pass

def create_app():
    with app.app_context():
        db_manager.init_db()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
