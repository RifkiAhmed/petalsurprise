#!/usr/bin/env python3
"""
User view for the API
"""
from api.v1.views import views
from datetime import datetime, timedelta
from flask import abort, jsonify, request, render_template
from models import storage, AUTH
from models.order import Order


FORMAT = "%Y-%m-%d %H:%M"


def _orders_data(orders):
    orders_data = []
    for order in orders:
        order_data = {
            'id': order.id,
            'created_at': datetime.strftime(
                order.created_at, FORMAT),
            'recipient_name': order.recipient_name,
            'recipient_address': order.recipient_address,
            'products_number': len(order.products),
            'message': order.message,
            'payment_method_type': order.payment_method_type,
            'status': order.status,
            'amount': int(order.amount) / 100,
            'products': []
        }
        for product in order.products:
            products_data = {
                'name': product.name,
                'image': product.img_path
            }
            order_data['products'].append(products_data)
        orders_data.append(order_data)
    return orders_data


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
    response.set_cookie("session_id", "",
                        expires=datetime.now() + timedelta(days=-1))
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


@views.route("/profile", methods=["PUT"])
def update_profile() -> str:
    """ Update user profile
    """
    session_id = request.cookies.get("session_id")
    email = request.form.get("email")
    username = request.form.get("username")
    current_password = request.form.get("currentPassword")
    new_password = request.form.get("password")
    if not session_id:
        abort(401)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
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


@views.route("/user_orders", methods=["GET"])
def user_activity() -> str:
    """ User orders history
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(401)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if not user:
            abort(403)
        orders = storage.find_all(Order, user_id=user.id)
        orders_data = _orders_data(orders)
        return jsonify(orders_data), 200
    except ValueError:
        abort(403)
