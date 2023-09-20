from functools import wraps
from flask import session, render_template, url_for, request, abort
from repositories.user_repository import user_repository


def logged_in(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if "username" not in session:
            return abort(401)

        return func(*args, **kwargs)
    return check_login


def csrf(func):
    @wraps(func)
    def check_csrf(*args, **kwargs):
        csrf_token = request.form.get("csrf_token")
        if session["csrf_token"] != csrf_token:
            abort(401)
        return func(*args, **kwargs)
    return check_csrf
