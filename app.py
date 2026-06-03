from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql
import ssl
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# TiDB Cloud Database Connection
def get_db_connection():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    return pymysql.connect(
        host="gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com",
        user="3C7PHDMsP5jWjoa.root",
        password="QvJqjH5XflBaKB7E",
        database="MetaMind",
        port=4000,
        ssl=ssl_context
    )


login_manage = LoginManager()
login_manage.init_app(app)
login_manage.login_view = "login"


class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = str(user_id)
        self.name = username
        self.email = email

    @staticmethod
    def get(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, email FROM users WHERE id = %s",
            (user_id,)
        )

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return User(result[0], result[1], result[2])

        return None


@login_manage.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, email, password FROM users WHERE email = %s",
            (email,)
        )

        user_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_data and user_data[3] == password:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Wrong email or password. Please try again."
        )

    return render_template("login.html")


@app.route("/Register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()

            return render_template(
                "register.html",
                error="This email is already registered. Please use another email."
            )

        cursor.execute(
            "INSERT INTO users(username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/psychology")
def about():
    return render_template("pysc.html")


@app.route("/philosophy")
def philosophy():
    return render_template("philosophy.html")


@app.route("/economics")
def economics():
    return render_template("economics.html")


@app.route("/Gametheory")
def gametheory():
    return render_template("gameth.html")


@app.route("/Historiography")
def history():
    return render_template("hist.html")


@app.route("/Evolutionary-Biology")
def bio():
    return render_template("eb.html")


@app.route("/anthropology")
def anthropology():
    return render_template("anthropology.html")


@app.route("/systems-thinking")
def systhinking():
    return render_template("systems-thinking.html")


@app.route("/linguistics")
def linguistics():
    return render_template("linguistics.html")


@app.route("/semiotics")
def semiotics():
    return render_template("semiotics.html")


@app.route("/ai-ethics")
def ai():
    return render_template("ai-ethics.html")


if __name__ == "__main__":
    app.run(debug=True)