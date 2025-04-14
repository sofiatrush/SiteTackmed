from flask import Flask, request, session, render_template, redirect, url_for, flash, jsonify
import os
import hashlib
import sqlite3
from database import DatabaseManager

class FirstAidApp:
    def __init__(self):
        self.app = Flask(__name__, template_folder='templates', static_folder='static')
        self.app.secret_key = "supersecretkey"
        DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')
        self.db_manager = DatabaseManager(DATABASE)

        self.setup_routes()

        @self.app.teardown_appcontext
        def close_db(error):
            self.db_manager.close_db(error)

    def run(self):
        with self.app.app_context():
            self.db_manager.init_db()
        self.app.run(debug=True)

    def setup_routes(self):
        app = self.app

        app.route("/")(self.home)
        app.route("/login", methods=["GET", "POST"])(self.login)
        app.route("/register", methods=["GET", "POST"])(self.register)
        app.route("/logout")(self.logout)
        app.route("/theory")(self.theory)
        app.route("/theory/Blood")(self.Blood)
        app.route("/theory/BloodHelp")(self.BloodHelp)
        app.route("/theory/ambulance")(self.ambulance)
        app.route("/theory/march")(self.march)
        app.route("/theory/burns")(self.burns)
        app.route("/theory/consciousness")(self.consciousness)
        app.route("/theory/examination")(self.examination)
        app.route("/theory/frostbite")(self.frostbite)
        app.route("/contacts")(self.contacts)
        app.route("/profile")(self.profile)
        app.route('/tests', methods=['GET'])(self.tests_menu)
        app.route('/test1')(self.test1_page)
        app.route('/test2')(self.test2_page)
        app.route('/test3')(self.test3_page)
        app.route('/submitTestResults', methods=['POST'])(self.submit_test_results)

    def home(self):
        name = session.get("name") if "email" in session else None
        return render_template("index.html", name=name)

    def login(self):
        if request.method == "POST":
            email = request.form["email"]
            password = hashlib.sha256(request.form["password"].encode()).hexdigest()
            db = self.db_manager.get_db()
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

    def register(self):
        if request.method == "POST":
            name = request.form["name"]
            surname = request.form["surname"]
            email = request.form["email"]
            password = hashlib.sha256(request.form["password"].encode()).hexdigest()
            db = self.db_manager.get_db()
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

    def logout(self):
        session.clear()
        flash("Ви вийшли з акаунту.", "info")
        return redirect(url_for("home"))

    def theory(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory_menu.html", name=name)

    def Blood(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/Blood.html", name=name)

    def BloodHelp(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/BloodHelp.html", name=name)

    def ambulance(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/ambulance.html", name=name)

    def march(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/march.html", name=name)

    def burns(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/burns.html", name=name)

    def consciousness(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/consciousness.html", name=name)

    def examination(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/examination.html", name=name)

    def frostbite(self):
        name = session.get("name") if "email" in session else None
        return render_template("theory/frostbite.html", name=name)

    def contacts(self):
        name = session.get("name") if "email" in session else None
        return render_template("contacts.html", name=name)

    def profile(self):
        if "email" not in session:
            return redirect(url_for("login"))
        db = self.db_manager.get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (session["email"],)).fetchone()
        if user:
            user_results = {}
            row = db.execute("SELECT * FROM results WHERE username = ?", (user["email"],)).fetchone()
            if row:
                user_results = {f'test{i}': row[f'test{i}'] for i in range(1, 9)}
            else:
                user_results = {f'test{i}': 0 for i in range(1, 9)}
            return render_template("profile.html", user=user, user_results=user_results)
        return redirect(url_for("login"))

    def tests_menu(self):
        user_results = {}
        name = session.get("name") if "email" in session else None
        if session.get("email"):
            username = session["email"]
            db = self.db_manager.get_db()
            row = db.execute("SELECT * FROM results WHERE username = ?", (username,)).fetchone()
            if row:
                user_results = {f'test{i}': row[f'test{i}'] for i in range(1, 9)}
            else:
                user_results = {f'test{i}': 0 for i in range(1, 9)}
        return render_template("tests_menu.html", user_results=user_results, name=name)

    def test1_page(self):
        name = session.get("name") if "email" in session else None
        return render_template("tests_frontend1.html", name=name)

    def test2_page(self):
        name = session.get("name") if "email" in session else None
        return render_template("tests_frontend2.html", name=name)

    def test3_page(self):
        name = session.get("name") if "email" in session else None
        return render_template("tests_frontend3.html", name=name)

    def submit_test_results(self):
        data = request.get_json()
        score = data.get('score')
        test_name = data.get('test_name')

        if 'email' not in session:
            return jsonify(message="Test taken, but result not saved (user not logged in)."), 200

        username = session['email']
        db = self.db_manager.get_db()
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

if __name__ == "__main__":
    app = FirstAidApp()
    app.run()
