import functools
from os import error

from flask import(
    Blueprint, flash, g, redirect, render_template, request, session
)

from werkzeug.security import check_password_hash, generate_password_hash
from db import exec, select

bp = Blueprint("auth", __name__, url_prefix="/auth")

MASTER_PASS = "aha"

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/")
        return view(**kwargs)
    return wrapped_view

@bp.before_app_first_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = select(
            "SELECT id FROM user WHERE id = %s", user_id
        )[0][0]

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("use_id")

    if user_id is None:
        g.user = None
    else:
        g.user = select(
            "SELECT * FROM user WHERE id = %s", user_id
        )[0][0]

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        error = None

        if not username:
            error = "ユーザー名を入力してください。"
        elif not password:
            error = "パスワードを入力してください。"
        elif select("SELECT id FROM user WHERE username = %s", username):
            error = "ユーザー名:{} は既に登録されています。".format(username)
        elif confirm != password:
            error = "パスワードが正しくありません。"
        
        if error is None:
            exec(
                "INSERT INTO user (username, password) VALUES (%s, %s)", 
                username, generate_password_hash(password)
            )
            return redirect("/auth/login?admin_pass={}".format(MASTER_PASS))
        
        flash(error)
    
    elif request.args.get("admin_pass", "") != MASTER_PASS:
        return redirect("/")

    return render_template("register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None
        
        user = select(
            "SELECT * FROM user WHERE username = %s", username
        )

        if not user:
            error = "ユーザー名が違います。"
        elif not check_password_hash(user[0][2], password):
            error = "パスワードが違います。"
        
        if error is None:
            session.clear()
            session["user_id"] = user[0][0]
            return redirect("/")
        
        flash(error)
    
    elif request.args.get("admin_pass", "") != MASTER_PASS:
        return redirect("/")
    
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")