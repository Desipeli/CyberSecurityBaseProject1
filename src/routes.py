from app import app
from flask import render_template, request, redirect, flash, url_for, abort
from services.requires import logged_in, csrf
from services.user_service import user_service
from services.moovie_service import moovie_service
from services.comment_service import comment_service


@app.route("/")
def index():
    moovies = moovie_service.get_moovies()
    return render_template("home.html", moovies=moovies)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if user_service.login(username, password):
            flash(f"Hello {username}")
            return redirect("/")
        else:
            flash("Invalid credentials")
            return render_template("login.html")


@app.route("/logout", methods=["POST"])
@csrf
def logout():
    user_service.logout()
    flash("logged out")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username").strip()
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        pw_validation_error = user_service.validate_passwords(
            password1, password2)
        if pw_validation_error:
            flash(pw_validation_error)
            return render_template("register.html")

        username_validation_error = user_service.validate_username(username)
        if username_validation_error:
            flash(username_validation_error)
            return render_template("register.html")

        if user_service.register_user(username, password1, ):
            return redirect("/")
        return render_template("error.html", error="Error while creating user")


@app.route("/moovie/<int:id>")
def moovie(id):
    scroll_to_comments = request.args.get("scroll_to_comments")
    moovie = moovie_service.get_moovie_by_id(id)
    comments = comment_service.get_comment_by_moovie(id).__reversed__()
    return render_template("moovie.html", moovie=moovie, comments=comments, scroll_to_comments=scroll_to_comments)


@app.route("/comment/<int:id>", methods=["POST"])
@logged_in
# @csrf
def comment(id):
    comment = request.form.get("comment")
    moovie = id
    try:
        comment_service.add_comment(
            comment, moovie
        )
        return redirect(url_for("moovie", id=id, scroll_to_comments=True))
    except Exception:
        flash("Error")
        return redirect(url_for("moovie", id=id, scroll_to_comments=False))


@app.route("/comment/delete/<int:id>", methods=["POST"])
@logged_in
@csrf
def delete_comment(id):
    moovie = request.form.get("moovie")
    if not comment_service.delete_comment(id):
        abort(401)
    return redirect(url_for("moovie", id=moovie, scroll_to_comments=True))
