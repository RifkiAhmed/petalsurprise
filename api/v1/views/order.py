#!/usr/bin/env python3
"""
Order view for the API
"""
from api.v1.views import views
from datetime import datetime
from flask import abort, jsonify, request
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
