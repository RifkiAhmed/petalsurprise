#!/usr/bin/env python3
"""
Index view for the API
"""
from api.v1.views import views
from flask import render_template, request
from models import storage, AUTH
from models.product import Product


@views.route('/')
def index():
    """Return index page"""
    session_id = request.cookies.get("session_id")
    user = None
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
    current_page = request.args.get('page', 1, type=int)
    per_page = 32
    products = storage.get_limit(Product, current_page - 1, per_page)
    serialized_products = [p.to_dict() for p in products]
    size = storage.count(Product)
    page = {'has_prev': True, 'has_next': True, 'num': current_page}

    if current_page == 1:
        page['has_prev'] = False
    if (current_page * per_page) >= size:
        page['has_next'] = False
    return render_template(
        'index.html',
        user=user,
        products=serialized_products,
        page=page)
