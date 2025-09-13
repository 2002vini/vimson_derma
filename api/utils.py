from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from vimson_derma import constants
from vimson_derma import settings


def send_email_handler(subject, recipient_email, html_content, attachments=None, cc=None):

    # Fallback plain text version
    text_content = strip_tags(html_content)

    # Send email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[recipient_email,],
        cc = cc or []
    )
    email.attach_alternative(html_content, "text/html")

    # Attach files if provided
    if attachments:
        for file_obj in attachments:
            email.attach(file_obj.name, file_obj.read(), file_obj.content_type)

    email.send()
    return f"Email sent"


def send_contact_mail(name, email, company_name, phone_number, category, message):
    """
    Sends a contact form submission email to Vimson Derma.
    """

    subject = f"New Contact Form Submission from : {name}"

    # Render into your HTML email template
    html_content = render_to_string(
        'EmailTemplate/contact_mail_template.html',
        {
            'name': name,
            'email': email,
            'company_name': company_name,
            'category': category,
            'contact_no': phone_number,
            'message': message
        }
    )
    send_email_handler(
        subject=subject,
        recipient_email=settings.EMAIL_HOST_USER,
        html_content=html_content,
        cc = [constants.SHRENIK_EMAIL, constants.KALPESH_EMAIL]
    )


def send_carrier_mail(name, email, dob, phone_number, position, file_field=None):
    subject = f"New Job Application - {position}"

    html_content = render_to_string(
        'EmailTemplate/contact_mail_template.html',
        {
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'dob': dob,
            'position': position,
        }
    )
    send_email_handler(
        subject = subject,
        recipient_email = settings.EMAIL_HOST_USER,
        html_content = html_content,
        attachments=[file_field] if file_field else None
    )


def send_quote_mail(name, email, contact_no, product_name, quantity, customization, message):
    subject = f"New Quote Request - {product_name}"

    html_content = render_to_string(
        'EmailTemplate/career_mail_template.html',
        {
            'name': name,
            'email': email,
            'contact_no': contact_no,
            'product_name': product_name,
            'quantity': quantity,
            'customization': customization,
            'message': message,
        }
    )
    send_email_handler(subject, settings.EMAIL_HOST_USER, html_content)
