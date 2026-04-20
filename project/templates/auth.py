from pathlib import Path

from flask import Flask, render_template, redirect, url_for


BASE_DIR = Path(__file__).resolve().parents[2]

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


@app.route("/")
def home_page():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("login/index.html")


@app.route("/login")
def login_page():
    return redirect(url_for("home"))


@app.route("/invalid-login")
def invalid_login_page():
    return render_template("invalid-login/index.html", login_link="/login")


@app.route("/user")
def user_login():
    return "Users (Students & Staffs) preview route"


@app.route("/maintenance")
def maintenance_login():
    return "Maintenance Staff preview route"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8084, debug=True)