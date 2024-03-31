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
    """ Add user to the database
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "This email is already registered"}), 400

    return jsonify({"message": "user created"}), 201


@views.route("/sessions", methods=["POST"])
def login() -> str:
    """ Create a session authentication for the user logged in
    """
    login = request.form.get("email")
    password = request.form.get("password")
    valid_lagin = AUTH.valid_login(password=password, email=login)

    session_id = None
    if not valid_lagin:
        valid_lagin = AUTH.valid_login(password=password, username=login)
        if not valid_lagin:
            abort(401)
        else:
            session_id = AUTH.create_session(username=login)
    else:
        session_id = AUTH.create_session(email=login)

    response = jsonify({})
    response.set_cookie("session_id", session_id)
    return response


@views.route("/sessions", methods=["DELETE"])
def logout() -> None:
    """ User logout by deleting the user's session
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user:
        abort(401)

    AUTH.destroy_session(user)
    response = jsonify({})
    response.set_cookie("session_id", "",
                        expires=datetime.now() + timedelta(days=-1))
    return response, 200


@views.route("/profile", methods=["GET"])
def profile() -> str:
    """ Returns user's profile
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    return render_template('/profile.html', user=user)


@views.route("/profile", methods=["PUT"])
def update_profile() -> str:
    """ Updates user's profile
    """
    email = request.form.get("email")
    username = request.form.get("username")
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("password")

    try:
        user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))

        if email:
            storage.update(user, email=email)
            return jsonify({"message": "Email updated"}), 200

        if username:
            storage.update(user, username=username)
            return jsonify({"message": "Username updated"}), 200

        if new_password:
            # returns True if valid login else False
            if not AUTH.valid_login(current_password, email=user.email):
                abort(401)
            AUTH.update_password(user, new_password=new_password)
            return jsonify({"message": "Password updated"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
