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
    orders_list = []
    for order in orders:
        order_dict = order.to_dict()
        order_dict["created_at"] = order_dict["created_at"].strftime(FORMAT)
        order_dict["amount"] /= 100
        order_dict["products"] = []
        for product in order.products:
            order_dict["products"].append(product.to_dict())
        order_dict["products_number"] = len(order.products)
        orders_list.append(order_dict)
    return orders_list


@views.route("/user_orders", methods=["GET"])
def user_activity() -> str:
    """ Returns user's orders
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))

    try:
        orders = storage.find_all(Order, user_id=user.id)
        orders_list = _orders_data(orders)
        return jsonify(orders_list), 200
    except NoResultFound:
        return jsonify({}), 200


@views.route("/dashboard/overview", methods=["GET"])
def dashboard_overview():
    """ Admin dashboard overview
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
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
            # stat[1]: Number of orders, stat[2]: Total amount
            status[stat[0]] = [stat[1], stat[2] // 100]

        stats_2_list = []
        for stat in stats_2:
            stat_dict = {
                "date": str(stat[0]),  # creation date
                "count": stat[1],  # orders count
                "total_amount": int(stat[2]) // 100}  # Total amount
            stats_2_list.append(stat_dict)

        return render_template(
            '/dashboard_overview.html',
            user=user,
            stats=status,
            data=stats_2_list)
    except NoResultFound:
        return render_template('/dashboard_overview.html', user=user)


@views.route("/orders", methods=["GET"])
def orders() -> str:
    """ Returns all orders with the specified status
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
        abort(403)

    status = request.args.get('status')
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    orders = None
    try:
        if status == 'Default':
            orders = storage.all(Order)
        else:
            orders = storage.find_all(Order, status=status)
    except NoResultFound:
        pass

    if from_date:
        from_date = datetime.fromisoformat(from_date)
        orders_from = [o for o in orders if o.created_at >= from_date]
        orders = orders_from

    if to_date:
        to_date = datetime.fromisoformat(to_date) + timedelta(days=1)
        orders_to = [o for o in orders if o.created_at <= to_date]
        orders = orders_to

    orders_list = _orders_data(orders)
    return jsonify(orders_list), 200


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


@views.route("/orders", methods=["PUT"])
def update_order() -> None:
    """ Update order status
    """
    from api.v1 import send_email

    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
        abort(403)

    id = request.form.get('id')
    status = request.form.get('status')
    order = storage.find_by(Order, id=id)

    if order:
        storage.update(order, status=status)

    if status == 'Delivered':
        send_email(
            subject="Order delivered",
            message=None,
            sender=None,
            receiver=order.user_email,
            order=order)

    return jsonify({}), 200
