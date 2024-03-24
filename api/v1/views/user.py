#!/usr/bin/env python3
"""
User view for the API
"""
from api.v1.views import views
from datetime import datetime, timedelta
from flask import abort, jsonify, request, render_template
from models import storage, AUTH


@views.route("/users", methods=["POST"])
def users() -> str:
    """User registration
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "This email is already registered"}), 400


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
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user:
        abort(403)
    AUTH.destroy_session(user)
    response = jsonify({})
    response.set_cookie("session_id", "",
                        expires=datetime.now() + timedelta(days=-1))
    return response


@views.route("/profile", methods=["GET"])
def profile() -> str:
    """ User profile
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user:
        abort(403)
    return render_template('/profile.html', user=user)


@views.route("/profile", methods=["PUT"])
def update_profile() -> str:
    """ Update user profile
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user:
        abort(403)
    email = request.form.get("email")
    username = request.form.get("username")
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("password")
    try:
        if username:
            storage.update(user, username=username)
            return jsonify({"message": "Username updated"}), 200
        if email:
            storage.update(user, email=email)
            return jsonify({"message": "Email updated"}), 200
        if new_password:
            if not AUTH.valid_login(user.email, current_password):
                abort(401)
            AUTH.update_password(user, new_password=new_password)
            return jsonify({"message": "Password updated"}), 200
    except ValueError:
        abort(403)
