#!/usr/bin/env python3
"""
Order view for the API
"""
from api.v1.views import views
from datetime import datetime
from flask import abort, jsonify, request, render_template
from models import storage, AUTH
from models.order import Order
from sqlalchemy.orm.exc import NoResultFound

FORMAT = "%Y-%m-%d %H:%M"


def _orders_data(orders):
    orders_data = []
    if not orders:
        return []
    for order in orders:
        order_data = {
            'charge_id': order.charge_id,
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
            'number_of_products': len(order.products),
            'products': []
        }
        for product in order.products:
            products_data = {
                'name': product.name,
                'image': product.img_path,
                'price': product.price
            }
            order_data['products'].append(products_data)
        orders_data.append(order_data)
    return orders_data


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


@views.route("/dashboard", methods=["GET"])
def dashboard() -> str:
    """ Admin dashboard
    """
    user = None
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    orders = []
    try:
        orders = storage.find_all(Order, status="Pending")
    except NoResultFound:
        pass
    return render_template('/dashboard.html', user=user, orders=orders)


@views.route("/orders", methods=["GET"])
def orders() -> str:
    """ Returns all orders with the specified status
    """
    user = None
    session_id = request.cookies.get("session_id")
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    orders = None
    status = request.args.get('status')
    try:
        if status == 'Default':
            orders = storage.all(Order)
        else:
            orders = storage.find_all(Order, status=status)
    except NoResultFound:
        pass
    orders_data = _orders_data(orders)
    return orders_data
