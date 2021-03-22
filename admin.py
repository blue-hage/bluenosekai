#!/usr/local/bin/python3
from logging import error
from os.path import join
from flask import(
    Blueprint, flash, g, redirect, render_template, request
)
import os, random, string

from auth import login_required
from db import exec, select
from blog import get_news, get_work

bp = Blueprint("admin", __name__, url_prefix="/admin")
UPLOAD_FOLDER='./static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

# news zone
@bp.route("/createnews", methods=["GET", "POST"])
@login_required
def createnews():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "タイトルを入力してください。"
        elif not body:
            error = "本文を入力してください。"
        
        if error is None:
            exec(
                "INSERT INTO news (title, body, author_id) VALUES (%s, %s, %s)",
                title, body, g.user
            )
            return redirect("/news")
        
        flash(error)
    
    return render_template("createnews.html")

@bp.route("/<int:id>/editnews", methods=["GET", "POST"])
@login_required
def editnews(id):
    news = get_news(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "タイトルを入力してください。"
        elif not body:
            error = "本文を入力してください。"
        
        if error is None:
            exec(
                "UPDATE news SET title = %s, body = %s WHERE id = %s",
                title, body, id
            )
            return redirect("/news")

        flash(error)

    return render_template("editnews.html", news=news)

@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    if request.method == "POST":
        get_news(id)
        exec("DELETE FROM news WHERE id = %s", id)
        return redirect("/news")


# work zone
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route("/creatework", methods=["GET", "POST"])
@login_required
def creatework():
    if request.method == "POST":
        title = request.form["title"]
        link = request.form["link"]
        error = None

        if not title:
            error = "タイトルを入力してください。"
        elif not link:
            error = "リンクを入力してください。"
        elif "work" not in request.files:
            error = "写真を選択してください。"
       
        # file confirmation 
        work = request.files["work"]
        if work.filename == "" or not allowed_file(work.filename):
            error = "写真を選択してください。"
        
        if error is not None:
            flash(error)
        else:
            workname = title + "_" + "".join(random.choice(string.ascii_letters + string.digits) for i in range(20)) + "." + work.filename.rsplit(".", 1)[1].lower()
            work.save(os.path.join(UPLOAD_FOLDER, workname))
            exec(
                "INSERT INTO work (title, link, work, author_id) VALUES (%s, %s, %s, %s)",
                title, link, workname, g.user
            )
            return redirect("/works")

    return render_template("creatework.html") 


@bp.route("/<int:id>/editwork", methods=["GET", "POST"])
@login_required
def editwork(id):
    work = get_work(id)

    if request.method == "POST":
        title = request.form["title"]
        link = request.form["link"]
        work = request.files["work"]
        error = None

        if not title:
            error = "タイトルを入力してください。"
        elif not link:
            error = "リンクを入力してください。"

        if error is not None:
            flash(error)
        else:
            if request.files["work"]:
                workname = title + "_" + "".join(random.choice(string.ascii_letters + string.digits) for i in range(20)) + "." + work.filename.rsplit(".", 1)[1].lower()
                work.save(os.path.join(UPLOAD_FOLDER, workname))
                work = select(
                    "SELECT * FROM work WHERE id = %s", id
                )[0]
                os.remove(os.path.join(UPLOAD_FOLDER, work[4]))
                exec(
                    "UPDATE work SET title = %s, work = %s, link = %s WHERE id = %s",
                    title, workname, link, id
                )

            else:
                exec(
                    "UPDATE work SET title = %s, link = %s WHERE id = %s",
                    title, link, id
                )
            return redirect("/works")

    return render_template("editwork.html", work=work)

@bp.route("/<int:id>/deletework", methods=["POST"])
@login_required
def deletework(id):
    work = get_work(id)
    if request.method == "POST":
        work = select(
            "SELECT * FROM work WHERE id = %s", id
        )[0]
        os.remove(os.path.join(UPLOAD_FOLDER, work[4]))
        exec("DELETE FROM work WHERE id = %s", id)
        return redirect("/works")
    return render_template("editwork.html", works=work)