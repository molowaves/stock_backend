from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_reg_otp(recipient, OTP, email, username):
    context = {
        "OTP":OTP,
        "username":username,
        "email":email
    }

    template_name = "templates/email.html"
    convert_to_html_content =  render_to_string(
    template_name=template_name,
    context=context
    )
    plain_message = strip_tags(convert_to_html_content)

    send_status = send_mail(
    subject="Company Name - User Enrollment",
    message=plain_message,
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[recipient],
    html_message=convert_to_html_content,
    fail_silently=True 
    )
