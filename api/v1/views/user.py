#!/usr/bin/env python3
"""
User view for the API
"""
from flask import abort, jsonify, request, render_template
from api.v1.views import views
from models.auth import Auth
from datetime import datetime, timedelta

AUTH = Auth()


@views.route("/users", methods=["POST"])
def users() -> str:
    """User registration
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        AUTH.register_user(email, password)
        return jsonify({"message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@views.route("/sessions", methods=["POST"])
def login() -> str:
    """User login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_lagin = AUTH.valid_login(email, password)
    if not valid_lagin:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@views.route("/sessions", methods=["DELETE"])
def logout() -> None:
    """User logout
    """
    user = None
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user)
    response = jsonify({})
    response.set_cookie(
        "session_id",
        "",
        expires=datetime.now() +
        timedelta(
            days=-
            1))
    return response


@views.route("/profile", methods=["GET"])
def profile() -> str:
    """ User profile
    """
    user = None
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return render_template('/profile.html', user=user, email=user.email)


@views.route("/reset_password", methods=["PUT"])
def update_password() -> str:
    """ User password reset
    """
    new_password = request.form.get("newPassword")
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(401)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        AUTH.update_password(user, new_password)
        return jsonify({"message": "Password updated"}), 200
    except ValueError:
        abort(403)
