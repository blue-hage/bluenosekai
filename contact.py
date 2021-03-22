#!/usr/local/bin/python3
from flask import(
    Blueprint, request, render_template, flash, redirect
)

from mail import contact_create

bp = Blueprint("contact", __name__, url_prefix="/contact")


@bp.route("/")
def index():
    return render_template("contact.html")

# contact zone
@bp.route("/question", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        confirm = request.form["confirm"]
        body = request.form["body"]
        error = None

        if not name:
            error = "名前を入力してください。"
        elif not email:
            error = "メールアドレスを入力してください。"
        elif not body:
            error = "お問い合わせ内容を入力してください。"
        elif confirm != email:
            error = "メールアドレスが違います。"

        if error is None:
            context={"name":name, "email":email, "body":body}
            return render_template("contact-confirm.html", context=context)
        
        flash(error)
        context={"name":name, "email":email, "body":body}
        return render_template("contact-form.html", context=context)
        
    return render_template("contact-form.html")

@bp.route("/send_contact", methods=["GET", "POST"])
def send_apply():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        body = request.form["body"]

        # exec("INSERT INTO contact (name, email, body) VALUES (%s, %s, %s)", name, email, body)
        contact_create(email, name, body)
        return redirect("/contact/msg/0")
    
    return render_template("contact-form.html")

#apply zone
@bp.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        confirm = request.form["confirm"]
        tel = request.form["tel"]
        which = request.form["which"]
        detail = request.form["detail"]
        budget = request.form["budget"]
        deadline = request.form["deadline"]
        body = request.form["body"]
        error = None

        if not name:
            error = "名前を入力してください。"
        elif not email:
            error = "メールアドレスを入力してください。"
        elif confirm != email:
            error = "メールアドレスが違います。"
        elif not tel:
            error = "電話番号を入力してください。"
        elif not which:
            error = "ご依頼内容を選択してください。"
        elif not detail:
            error = "ご依頼内容を入力してください。"
        elif not budget:
            error = "想定予算を入力してください。"
        elif not deadline:
            error = "ご希望納期を選択してください。"
        elif not body:
            error = "目的・概要を入力してください。"


        if error is None:
            context = {"name":name, "email":email, "tel":tel, "which":which, "detail":detail, "budget":budget, "deadline":deadline, "body":body}
            return render_template("apply-confirm.html", context=context)
        
        flash(error)
        context = {"name":name, "email":email, "tel":tel, "which":which, "detail":detail, "budget":budget, "deadline":deadline, "body":body}
        return render_template("apply-form.html", context=context)
    
    return render_template("apply-form.html")

@bp.route("/send_application", methods=["GET", "POST"])
def send_application():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        tel = request.form["tel"]
        which = request.form["which"]
        detail = request.form["detail"]
        budget = request.form["budget"]
        deadline = request.form["deadline"]
        body = request.form["body"]

        # exec("INSERT INTO contact (name, email, tel, detail, budget, deadline, body) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
        # name, email, tel, detail, budget, deadline, body)
        contact_create(email, name, body, tel, which, detail, budget, deadline, body)
        return redirect("/contact/msg/1")
    
    return render_template("apply-form.html")

@bp.route("/msg/<int:id>")
def msg(id):
    if id == 0:
        return render_template("msg.html", title="お問い合わせ", sub="Contact Form", message="お問い合わせ")
    elif id == 1:
        return render_template("msg.html", title="制作依頼", sub="Request Form", message="制作依頼のお申し込み")
    else:
        return redirect("/")