#!/usr/bin/env python3
"""
Order view for the API
"""
from api.v1.views import views
from datetime import datetime, timedelta
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
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user:
        abort(401)
    try:
        orders = storage.find_all(Order, user_id=user.id)
        _orders = _orders_data(orders)
        return _orders, 200
    except ValueError:
        abort(403)


@views.route("/dashboard/overview", methods=["GET"])
def dashboard_overview() -> str:
    """ Admin dashboard
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(403)
    try:
        stats_1, stats_2 = storage.orders_overview(Order)
        status = {
            "Pending": None,
            "Delivering": None,
            "Delivered": None,
            "Cancelled": None,
            "Refunded": None}
        i = 0
        for stat in stats_1:
            status[stat[0]] = [stat[1], stat[2] // 100]
        stats_2_dicts = []
        for stat in stats_2:
            stat_dict = {
                "date": str(
                    stat[0]), "count": stat[1], "total_amount": int(
                    stat[2]) // 100}
            stats_2_dicts.append(stat_dict)
        return render_template(
            '/dashboard_overview.html',
            user=user,
            stats=status,
            data=stats_2_dicts)
    except NoResultFound:
        return render_template('/dashboard_overview.html', user=user)


@views.route("/dashboard/orders", methods=["GET"])
def dashboard_orders() -> str:
    """ Admin dashboard
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(403)
    orders = []
    try:
        orders = storage.find_all(Order, status="Pending")
    except NoResultFound:
        pass
    return render_template('/dashboard_orders.html', user=user, orders=orders)


@views.route("/orders", methods=["GET"])
def orders() -> str:
    """ Returns all orders with the specified status
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(403)
    orders = None
    status = request.args.get('status')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    try:
        if status == 'Default':
            orders = storage.all(Order)
        else:
            orders = storage.find_all(Order, status=status)
    except NoResultFound:
        pass
    orders_data = orders
    if from_date:
        from_date = datetime.fromisoformat(from_date)
        orders_from = [o for o in orders if o.created_at >= from_date]
        orders_data = orders_from
    if to_date:
        to_date = datetime.fromisoformat(to_date) + timedelta(days=1)
        orders_to = [o for o in orders_data if o.created_at <= to_date]
        orders_data = orders_to
    orders_data_dict = _orders_data(orders_data)
    return orders_data_dict


@views.route("/orders", methods=["PUT"])
def update_order() -> str:
    """ Update order status
    """
    from api.v1 import send_email
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(403)
    id = request.form.get('id')
    status = request.form.get('status')
    order = storage.find_by(Order, id=id)
    if order:
        storage.update(order, status=status)
    if status == 'Delivered':
        send_email(
            subject="Order delivered",
            message="",
            sender=None,
            receiver=order.user_email,
            order=order)
    return jsonify({})
