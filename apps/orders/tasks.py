from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_order_confirmation_email(order_id, user_email):
    subject = f"Order #{order_id} Confirmed"
    message = "Thank you for your purchase! Your order is being processed."
    send_mail(subject, message, "admin@marketplace.com", [user_email])
    return f"Email sent to {user_email}"
