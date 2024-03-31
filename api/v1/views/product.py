#!/usr/bin/env python3
"""
Product view for the API
"""
from api.v1.views import views
from datetime import datetime
from flask import jsonify, request, abort
from models.product import Product
from models import storage, AUTH
import os
from sqlalchemy.orm.exc import NoResultFound

FORMAT = '%Y%m%d%H%M%S'
PATH = 'api/v1/static/flowers'


def _flower_data():
    """ Validates and returns the folwer data
    """
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image = request.files.get('image')

    if not name:
        return ({"error": "Flower name cannot be empty"}, 400)

    try:
        price = int(price)
    except ValueError:
        return ({"error": "Price must be an integer greater than 0"}, 400)

    data = {"name": name, "price": int(price), "description": description}

    if image:
        file_extension = os.path.splitext(image.filename)[1]
        if file_extension not in ['.jpg', '.png']:
            return ({"error": "Image extension must be .jpg or .png"}, 400)
        filename = f'img_{datetime.now().strftime(FORMAT)}{file_extension}'
        file_path = f'{PATH}/{filename}'
        image.save(file_path)
        data["filename"] = filename

    return data


@views.route("/product/<id>", methods=["GET"])
def get_product(id) -> str:
    """ Returns the product object with the id parameter
    """
    try:
        product = storage.find_by(Product, id=id)
    except NoResultFound as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(product.to_dict()), 200


@views.route("/products", methods=["POST"])
def add_products() -> str:
    """ Add new Product object to the database
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
        abort(403)

    try:
        data = _flower_data()
        if len(data) == 2:
            return jsonify(data[0]), data[1]

        product = Product(**data)
        storage.add(product)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"message": "Product added successfully"}), 201


@views.route("/products", methods=["DELETE"])
def delete_product() -> str:
    """ Delist product object
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
        abort(403)

    try:
        id = request.form.get('id')
        product = storage.find_by(Product, id=id)
        storage.update(product, listed=False)
        return jsonify({"message": "Product delisted"}), 200
    except NoResultFound as e:
        return jsonify({"error": str(e)}), 404


@views.route("/products", methods=["PUT"])
def update_product() -> str:
    """ Update Product
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
        abort(403)

    try:
        data = _flower_data()
        if len(data) == 2:
            return jsonify(data[0]), data[1]

        id = request.form.get('id')
        product = storage.find_by(Product, id=id)

        if data.get("image"):
            os.remove(f'{PATH}/{product.filename}')

        storage.update(product, **data)
    except (NoResultFound, FileNotFoundError) as e:
        return jsonify({"error": str(e)}), 404

    return jsonify({"message": "Product updated successfully"}), 200
