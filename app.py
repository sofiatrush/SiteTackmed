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
    name = session.get("name") if "email" in session else None
    return render_template("index.html", name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        db = db_manager.get_db()
        user = db.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
                         (email, password)).fetchone()

        if user:
            session["email"] = user["email"]
            session["name"] = user["name"]
            flash("Вхід успішний!", "success")
            return redirect(url_for("home"))
        else:
            flash("Неправильний email або пароль", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = hashlib.sha256(request.form["password"].encode()).hexdigest()

        db = db_manager.get_db()
        try:
            db.execute("INSERT INTO users (name, surname, email, password) VALUES (?, ?, ?, ?)",
                      (name, surname, email, password))
            db.commit()
            session["email"] = email
            session["name"] = name
            flash("Реєстрація успішна!", "success")
            return redirect(url_for("home"))
        except sqlite3.IntegrityError:
            flash("Цей email вже зареєстрований!", "danger")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Ви вийшли з акаунту.", "info")
    return redirect(url_for("home"))

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
