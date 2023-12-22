from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session

from serializer.accounts import AccountSchema, AccountLogin
from service.accounts import AccountService

account_blueprint = Blueprint('account', __name__)
account_service = AccountService()


@account_blueprint.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        re_password = request.form.get("re_password")

        if password != re_password:
            return render_template("register.html", error="Passwords not match")

        data = AccountSchema(full_name=full_name, email=email, password=password, nickname=nickname)
        account_service.create_account(data)
        return redirect(url_for("account.login"))

    return render_template("register.html")


@account_blueprint.route("/", methods=["POST", "GET"])
def login():
    try:
        session.clear()
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            data = AccountLogin(email=email, password=password)

            user = account_service.login(data)
            session["name"] = user
            return redirect(url_for("home"))
        return render_template("login.html")

    except ValueError as e:
        return render_template("login.html", error=str(e))
