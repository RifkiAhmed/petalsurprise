#!/usr/bin/env python3
"""
Index view for the API
"""
from api.v1.views import views
from flask import render_template, request
from models import storage, AUTH
from models.product import Product
import os

@views.route('/', methods=['GET', 'POST'])
def index():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    current_page = request.args.get('page', 1, type=int)
    per_page = 32
    min_price = request.form.get('min-price', type=float)
    max_price = request.form.get('max-price', type=float)
    search_with_name = request.form.get('search-string')
    products = []
    if min_price or max_price:
        products = storage.get_range_filter(Product, min_price, max_price)
    elif search_with_name:
        products = storage.get_string_filter(Product, search_with_name)
    else:
        products = storage.get_limit(Product, current_page - 1, per_page)
    serialized_products = [p.to_dict() for p in products]
    size = storage.count(Product)
    page = {'has_prev': True, 'has_next': True, 'num': current_page}
    if current_page == 1:
        page['has_prev'] = False
    if (current_page * per_page) >= size:
        page['has_next'] = False
    return render_template('index.html', user=user,
                           products=serialized_products, page=page)


@views.route('/index/products/<sort_by>', methods=['GET'])
def products_sorted(sort_by):
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    current_page = request.args.get('page', 1, type=int)
    per_page = 32
    products = []
    products = storage.get_limit(Product, current_page - 1, per_page, sort_by)
    serialized_products = [p.to_dict() for p in products]
    size = storage.count(Product)
    page = {'has_prev': True, 'has_next': True, 'num': current_page}
    if current_page == 1:
        page['has_prev'] = False
    if (current_page * per_page) >= size:
        page['has_next'] = False
    return {
        "products": serialized_products,
        "page": page,
        "user": user.to_dict()}


@views.route('/contact', methods=["GET"])
def contact():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    return render_template('contact.html', user=user)


@views.route('/contact', methods=["POST"])
def send_email():
    """Return index page"""
    from api.v1 import send_email
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    send_email(
        subject=subject,
        message=message,
        sender=email,
        receiver=os.getenv('USER_MAIL'))
    return ({"message": "Message sent successfully!"})


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
