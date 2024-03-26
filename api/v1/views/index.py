#!/usr/bin/env python3
"""
Index view for the API
"""
from api.v1.views import views
from flask import render_template, request, redirect, url_for
from models import storage, AUTH
from models.product import Product
import os


@views.route('/', methods=['GET', 'POST'])
def index():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    current_page = request.args.get('page', 1, type=int)
    products = []
    products = storage.get_limit(
        Product, current_page - 1, int(os.getenv('PER_PAGE')), 'index')
    serialized_products = [p.to_dict() for p in products]
    size = storage.count(Product)
    page = {'has_prev': True, 'has_next': True, 'num': current_page}
    if current_page == 1:
        page['has_prev'] = False
    if (current_page * int(os.getenv('PER_PAGE'))) >= size:
        page['has_next'] = False
    return render_template('index.html', user=user,
                           products=serialized_products, page=page)


@views.route('/range', methods=['GET', 'POST'])
def range():
    """Return index page"""
    print('hhhh')
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    min_price = request.form.get('min_price', type=float)
    max_price = request.form.get('max_price', type=float)
    print(min_price)
    products = []
    if not min_price and not max_price:
        print('redirect')
        return redirect(url_for('views.index'))
    products = storage.get_range_filter(Product, min_price, max_price)
    serialized_products = [p.to_dict() for p in products]
    page = {'has_prev': False, 'has_next': False, 'num': 1}
    return {
        "products": serialized_products,
        "page": page,
        "user": user.to_dict()}


@views.route('/search', methods=['GET', 'POST'])
def string_search():
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    search_with_name = request.form.get('search-string')
    products = []
    if not search_with_name:
        return redirect(url_for('views.index'))
    products = storage.get_string_filter(Product, search_with_name)
    serialized_products = [p.to_dict() for p in products]
    page = {'has_prev': False, 'has_next': False, 'num': 1}
    return render_template(
        'index.html',
        user=user,
        products=serialized_products,
        page=page)


@views.route('/index/products/<sort_by>', methods=['GET'])
def products_sorted(sort_by):
    """Return index page"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    products = []
    products = storage.get_limit(
        cls=Product,
        page=None,
        per_page=None,
        sort_by=sort_by)
    serialized_products = [p.to_dict() for p in products]
    page = {'has_prev': False, 'has_next': False, 'num': 1}
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
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    from api.v1 import send_email
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')
    if not email:
        email = user.email
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
