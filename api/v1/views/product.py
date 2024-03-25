#!/usr/bin/env python3
"""
Product view for the API
"""
from api.v1.views import views
from datetime import datetime
from flask import jsonify, redirect, request, abort
from models.product import Product
from models import storage, AUTH
import os

FORMAT = '%Y%m%d%H%M%S'
PATH = 'api/v1/static/flowers'


@views.route("/products", methods=["POST"])
def add_products() -> str:
    """ Add new Product object to the storage
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(401)
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.files['image']
    file_extension = os.path.splitext(image.filename)[1]
    filename = f'img_{datetime.now().strftime(FORMAT)}{file_extension}'
    file_path = f'{PATH}/{filename}'
    try:
        product = Product(name=name, price=int(price), img_path=filename)
        storage.add(product)
        image.save(file_path)
        return redirect('/')
    except Exception as e:
        return jsonify({"message": e.message})


@views.route("/products", methods=["DELETE"])
def delete_product() -> str:
    """ Remove Product object from the storage
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(401)
    id = request.form.get('id')
    try:
        product = storage.find_by(Product, id=id)
        storage.delete(product)
        return jsonify({"message": "Product deleted"})
    except Exception as e:
        return jsonify({"message": e.message})


@views.route("/products", methods=["PUT"])
def update_product() -> str:
    """ Update Product
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user or not user.is_admin:
        abort(401)
    id = request.form.get('id')
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.files.get('image')
    try:
        product = storage.find_by(Product, id=id)
        if image:
            os.remove(f'{PATH}/{product.img_path}')
            file_extension = os.path.splitext(image.filename)[1]
            filename = f'img_{datetime.now().strftime(FORMAT)}{file_extension}'
            file_path = f'{PATH}/{filename}'
            image.save(file_path)
            storage.update(product, name=name,
                           price=int(price), img_path=filename)
        else:
            storage.update(product, name=name, price=int(price))
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        return jsonify({"message": e.message})
