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
    name = session.get("name") if "email" in session else None
    return render_template("theory_menu.html", name=name)

@app.route("/theory/Blood")
def Blood():
    name = session.get("name") if "email" in session else None
    return render_template("theory/Blood.html", name=name)

@app.route("/theory/BloodHelp")
def BloodHelp():
    name = session.get("name") if "email" in session else None
    return render_template("theory/BloodHelp.html", name=name)

@app.route("/theory/ambulance")
def ambulance():
    name = session.get("name") if "email" in session else None
    return render_template("theory/ambulance.html", name=name)

@app.route("/theory/march")
def march():
    name = session.get("name") if "email" in session else None
    return render_template("theory/march.html", name=name)

@app.route("/theory/burns")
def burns():
    name = session.get("name") if "email" in session else None
    return render_template("theory/burns.html", name=name)

@app.route("/theory/consciousness")
def consciousness():
    name = session.get("name") if "email" in session else None
    return render_template("theory/consciousness.html", name=name)

@app.route("/theory/examination")
def examination():
    name = session.get("name") if "email" in session else None
    return render_template("theory/examination.html", name=name)

@app.route("/theory/frostbite")
def frostbite():
    name = session.get("name") if "email" in session else None
    return render_template("theory/frostbite.html", name=name)

@app.route("/contacts")
def contacts():
    name = session.get("name") if "email" in session else None
    return render_template("contacts.html", name=name)

@app.route("/profile")
def profile():
    if "email" not in session:
        return redirect(url_for("login"))

    db = db_manager.get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (session["email"],)).fetchone()
    if user:
        user_results = {}
        db = db_manager.get_db()
        row = db.execute("SELECT * FROM results WHERE username = ?", (user["email"],)).fetchone()
        if row:
            user_results = {f'test{i}': row[f'test{i}'] for i in range(1, 9)}
        else:
            user_results = {f'test{i}': 0 for i in range(1, 9)}
        return render_template("profile.html", user=user, user_results=user_results)
    return redirect(url_for("login"))

@app.route('/tests', methods=['GET'])
def tests_menu():
    user_results = {}
    name = session.get("name") if "email" in session else None
    if session.get("email"):
        username = session["email"]
        db = db_manager.get_db()
        row = db.execute("SELECT * FROM results WHERE username = ?", (username,)).fetchone()
        if row:
            user_results = {f'test{i}': row[f'test{i}'] for i in range(1, 9)}
        else:
            user_results = {f'test{i}': 0 for i in range(1, 9)}
    return render_template("tests_menu.html", user_results=user_results, name=name)

app.route('/test1')
def test1_page():
    name = session.get("name") if "email" in session else None
    return render_template("tests_frontend1.html", name=name)

@app.route('/test2')
def test2_page():
    name = session.get("name") if "email" in session else None
    return render_template("tests_frontend2.html", name=name)

@app.route('/submitTestResults', methods=['POST'])
def submit_test_results():
    data = request.get_json()
    score = data.get('score')
    test_name = data.get('test_name')

    if 'email' not in session:
        return jsonify(message="Test taken, but result not saved (user not logged in)."), 200

    username = session['email']
    db = db_manager.get_db()
    row = db.execute("SELECT * FROM results WHERE username = ?", (username,)).fetchone()

    if row:
        current_score = row[test_name]
        if score > current_score:
            db.execute(f"UPDATE results SET {test_name} = ? WHERE username = ?", (score, username))
            db.commit()
            return jsonify(message="Test result updated."), 200
        return jsonify(message="Test result not updated"), 200
    else:
        tests = {f"test{i}": 0 for i in range(1, 9)}
        tests[test_name] = score
        db.execute('''
            INSERT INTO results (username, test1, test2, test3, test4, test5, test6, test7, test8)
            VALUES (:username, :test1, :test2, :test3, :test4, :test5, :test6, :test7, :test8)
        ''', {"username": username, **tests})
        db.commit()
        return jsonify(message="Test result saved."), 201

def create_app():
    with app.app_context():
        db_manager.init_db()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
