#!/usr/bin/env python3
"""
Product view for the API
"""
from flask import jsonify, redirect, request
from api.v1.views import views
from models.product import Product
from models import storage
from datetime import datetime
import os

FORMAT = "%Y%m%d%H%M%S"


@views.route("/products", methods=["POST"])
def add_products() -> str:
    """ Add new Product object to the storage
    """
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.files['image']
    file_extension = os.path.splitext(image.filename)[1]
    filename = f'img_{datetime.now().strftime(FORMAT)}{file_extension}'
    file_path = f'api/v1/static/products/{filename}'
    product = Product(name=name, price=int(price), img_path=filename)
    storage.add(product)
    image.save(file_path)
    return redirect('/')


@views.route("/products", methods=["DELETE"])
def delete_product() -> str:
    """ Remove Product object from the storage
    """
    id = request.form.get('id')
    product = storage.find_by(Product, id=id)
    storage.delete(product)
    return jsonify({"message": "Product deleted"})


@views.route("/products", methods=["PUT"])
def update_product() -> str:
    """ Update Product
    """
    id = request.form.get('id')
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.files.get('image')
    product = storage.find_by(Product, id=id)
    if image:
        os.remove(f'api/v1/static/products/{product.path}')
        file_extension = os.path.splitext(image.filename)[1]
        filename = f'img_{datetime.now().strftime(FORMAT)}{file_extension}'
        file_path = f'api/v1/static/products/{filename}'
        image.save(file_path)
        storage.update(product, name=name, price=int(price), img_path=filename)
    else:
        storage.update(product, name=name, price=int(price))

    return jsonify({"message": "Product updated successfully"})
