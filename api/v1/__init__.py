#!/usr/bin/env python3
"""
Send email function
"""
from datetime import datetime
from email.message import EmailMessage
import os
import smtplib
import ssl


def send_email(subject, message, sender=None, receiver=None, order=None):
    """Sends and receive emails to and from sustomers
    """
    USER_MAIL = os.getenv('USER_MAIL')
    USER_PWD = os.getenv('USER_PWD')
    flowers = ''
    if order:
        flowers = 'Flowers: ' if len(order.products) > 1 else 'Flower: '
        flowers += ', '.join(product.name for product in order.products)
    
    html_content = ""
    head = f"""
        <head>
            <style>
                .content {{
                    background-color: #14213d;;
                    padding: 50px 20px;
                    max-width: 900px;
                    margin: auto;
                    
                }}
                
                img {{
                    width: 300px;
                    display: block;
                    margin: auto;
                }}
                
                .header, .message {{
                    background-color: rgba(109, 89, 122, 0.4);
                    color: #ffffff;
                    max-width: 700px;
                    padding:10px 15px;
                    border-radius: 8px;
                    margin: 10px auto;
                }}
                
                .message {{
                    margin: 0px auto 50px;
                }}
                
                h3, h4, h3#customer_email {{
                    color: #ffffff;
                }}
                
                a#website_url {{
                    display: block;
                    text-align: center;
                    font-size: 18px;
                    font-weigth: bold;
                    color: #ffffff;
                }}
            </style>
        </head>
    """
    if sender:
        body = f"""
            <body>
                <div class="content" >
                    <img src="{ os.getenv('BRAND') }">
                    <div class="header">
                        <h3 id="customer_email">From: { sender }</h3>
                        <h3>Subject: { subject }</h3>
                    </div>
                    <div class="message">
                        <h3>Message:</h3>
                        <h4>{ message }</h4>
                    </div>
                    <a id="website_url" href="http://localhost:5000/">PetalSurprise</a>
                </div>
            </body>
        """
        html_content = f'<!DOCTYPE html><html lang="us">{head}{body}</html>'
    elif receiver:
        body = f"""
            <body>
                <div class="content" >
                    <img src="{ os.getenv('BRAND') }">
                    <div class="header">
                        <h3>Order delivered</h3>
                        <h3>Created at: { order.created_at }</h3>
                    </div>
                    <div class="message">
                        <h3>Hello Dear Customer,</h3>
                        <h4>We are delighted to inform you that your order has been successfully delivered!</h4>
                        <h3>Order Details:</h3>
                        <h4> - Recipient's name: { order.recipient_name }</h4>
                        <h4> - Delivery Address: { order.recipient_address }</h4>
                        <h4> - Message sent: { order.message }</h4>
                        <h4> - { flowers }</h4>
                        <br>
                        <br>
                        <h4>Thank you for choosing us to deliver your special gift.
                        If you have any feedback or need further assistance,
                        please don't hesitate to contact us.
                        We look forward to serving you again soon!</h4>
                        <h3>Best regards,</h3>
                    </div>
                    <a id="website_url" href="http://localhost:5000/">PetalSurprise</a>
                </div>
            </body>
        """
        html_content = f'<!DOCTYPE html><html lang="us">{head}{body}</html>'
    email = EmailMessage()
    email['From'] = USER_MAIL
    email['Subject'] = subject
    email['To'] = receiver
    email.add_alternative(html_content, subtype='html')

    context = ssl.create_default_context()
    host = 'smtp.gmail.com'
    port = 465
    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(USER_MAIL, USER_PWD)
        smtp.send_message(email)
