#!/usr/bin/env python3
"""
Index view for the API
"""
from api.v1.views import views
from flask import render_template, request, redirect, url_for, jsonify
from models import storage, AUTH
from models.product import Product
import os


@views.route('/', methods=['GET'])
def index():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    current_page = request.args.get('page', 1, type=int)
    per_page = int(os.getenv('PER_PAGE'))

    products, count_listed = storage.get_limit(
        cls=Product, page=current_page - 1, per_page=per_page)
    products_list = [p.to_dict() for p in products]

    page = {'num': current_page}
    page['has_prev'] = True if current_page > 1 else False
    end_index = current_page * per_page
    page['has_next'] = True if end_index < count_listed else False

    return render_template('index.html', user=user,
                           products=products_list, page=page)


@views.route('/range', methods=['GET'])
def range():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)

    if not min_price and not max_price:
        return redirect(url_for('views.index'))

    products = storage.get_range_filter(Product, min_price, max_price)
    products_list = [p.to_dict() for p in products]

    user = user.to_dict() if user else None
    return jsonify({"products": products_list, "user": user}), 200


@views.route('/search', methods=['GET'])
def search():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    name = request.args.get('name')

    if not name:
        return redirect(url_for('views.index'))

    products = storage.get_string_filter(Product, name)
    products_list = [p.to_dict() for p in products]

    user = user.to_dict() if user else None
    return jsonify({"products": products_list, "user": user}), 200


@views.route('/products_sorted', methods=['GET'])
def products_sorted():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    sort_by = request.args.get('sort_by')

    products, _ = storage.get_limit(cls=Product, page=None, per_page=None,
                                    sort_by=sort_by)
    products_list = [p.to_dict() for p in products]

    user = user.to_dict() if user else None
    return jsonify({"products": products_list, "user": user}), 200


@views.route('/contact', methods=["GET"])
def contact():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    return render_template('contact.html', user=user)


@views.route('/contact', methods=["POST"])
def send_email():
    """Return index page"""
    from api.v1 import send_email

    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not email:
        email = user.email

    receiver = os.getenv('USER_MAIL')
    send_email(subject=subject, message=message, sender=email,
               receiver=receiver)

    return jsonify({"message": "Message sent successfully!"}), 200


@views.route('/about')
def about():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    return render_template('about.html', user=user)


@views.route('/auth')
def auth():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    return render_template('auth.html', user=user)
