#!/usr/bin/env python3
"""
Checkout view for the API
"""
from api.v1.views import views
from flask import jsonify, request, abort
from models import storage, AUTH
from models.order import Order
from models.product import Product
import os
import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')


@views.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """ Create Stripe checkout session and return it's id
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    data = request.get_json()
    cart = data.get('cart', [])
    sender_email = data.get('sender_email')
    recipient_name = data.get('recipient_name')
    recipient_address = data.get('recipient_address')
    message = data.get('message', '')

    list_items = []
    products_ids = []
    for item in cart:
        products_ids.append(item['id'])
        line_item = {
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item['name'], },
                'unit_amount': int(item['price']) * 100,
            },
            'quantity': 1,
        }
        list_items.append(line_item)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=list_items,
        payment_intent_data={'metadata': {
            'user_id': str(user.id) if user else None,
            'user_email': user.email if user else sender_email,
            'recipient_name': recipient_name,
            'recipient_address': recipient_address,
            'message': message,
            'products': ', '.join(map(str, products_ids))}
        },
        mode='payment',
        success_url='https://petalsurprise.store',
        cancel_url='https://petalsurprise.store',
    )

    return jsonify({'sessionId': session.id})


@views.route('/webhook', methods=['POST'])
def stripe_webhook():
    """ handling webhook payment_intent.succeeded event
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('WEBHOOK_SIGNING_SECRET'))
    except ValueError as e:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle payment_intent.succeeded event
    if event['type'] == 'payment_intent.succeeded':
        # print(event)
        payment_intent = event['data']['object']
        charge_id = payment_intent.get('latest_charge')
        payment_method_type = payment_intent.get('payment_method_types')
        amount = int(payment_intent.get('amount_received'))
        currency = payment_intent.get('currency')
        payment_metadata = payment_intent.get('metadata', {})
        user_id = payment_metadata.get('user_id')
        user_email = payment_metadata.get('user_email')
        recipient_name = payment_metadata.get('recipient_name')
        recipient_address = payment_metadata.get('recipient_address')
        message = payment_metadata.get('message')
        products_ids = payment_metadata.get('products').split(', ')

        order = Order(user_id=user_id, user_email=user_email,
                      recipient_name=recipient_name,
                      recipient_address=recipient_address, message=message,
                      payment_method_type=payment_method_type, amount=amount,
                      currency=currency, charge_id=charge_id)
        storage.add(order)

        for product_id in products_ids:
            product = storage.find_by(Product, id=int(product_id))
            order.products.append(product)
        storage.save()

    return 'Success', 200


@views.route('/refund', methods=['PUT'])
def charge_refund():
    """ Refund customer
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if not user.is_admin:
        abort(403)

    order_id = request.form.get('orderId')
    charge_id = request.form.get('chargeId')
    if order_id and charge_id:
        try:
            stripe.Refund.create(charge=charge_id,)
            order = storage.find_by(Order, id=order_id)
            storage.update(order, status="Refunded")
        except Exception as e:
            return jsonify({"error": e.message}), 400

    return jsonify({}), 200
