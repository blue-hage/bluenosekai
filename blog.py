#!/usr/local/bin/python3
from os import error
from flask import(
    Blueprint, flash, g, redirect, render_template, request
)
from werkzeug.exceptions import abort

from auth import login_required
from db import select
from mail import contact_create

bp = Blueprint("blog", __name__)

# index
@bp.route("/")
def index():
    return render_template("index.html")

# news
@bp.route("/news")
def news():
    # news = select(
    #     "SELECT news.id, title, body, created, author_id, username FROM news JOIN user ON news.author_id = user.id ORDER BY created DESC"
    # )

    # if not news:
    #     length = 0
    # else:
    #     length = len(news)
        
    # news=news, length=lengthをあとでたす。
    return render_template("news.html")

def get_news(id, check_author=True):
    news = select(
        "SELECT news.id, title, body, created, author_id, username"
        " FROM news JOIN user ON news.author_id = user.id"
        " WHERE news.id = %s", 
        id
    )[0]

    if not news:
        abort(404, "News id {} doesn't exist.".format(id))
    
    return news

# About us
@bp.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

# works
def get_work(id, check_author=True):
    work = select(
        "SELECT work.id, title, link, work, created, author_id, username"
        " FROM work JOIN user ON work.author_id = user.id"
        " WHERE work.id = %s", 
        id
    )[0]

    if not work:
        abort(404, "work id {} doesn't exist.".format(id))
    
    return work

@bp.route("/works")
def works():
    # works = select(
    #     "SELECT work.id, title, link, work, created, author_id, username"
    #     " FROM work JOIN user ON work.author_id = user.id ORDER BY created DESC"
    # )
    
    # if works:
    #     length = len(works)
    # else:
    #     works = None
    #     length = 0

    # works=works, length=lengthをあとでたす。
    return render_template("works.html")

@bp.route("/service")
def service():
    return render_template("service.html")

@bp.route("/site_policy")
def site_policy():
    return render_template("site-policy.html")

@bp.route("/privacy_policy")
def plivacy_policy():
    return render_template("privacy-policy.html")