from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from vimson_derma import settings


def send_email_handler(subject, recipient_email, html_content):

    # Fallback plain text version
    text_content = strip_tags(html_content)

    # Send email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[recipient_email,]
    )
    email.attach_alternative(html_content, "text/html")
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
            'subject': subject,
            'name': name,
            'email': email,
            'company_name': company_name,
            'category': category,
            'contact_no': phone_number,
            'message': message
        }
    )
    send_email_handler(subject, settings.EMAIL_HOST_USER, html_content)


def send_carrier_mail(recipient_name, recipient_email):
    subject = "Wallet Withdrawal Request Received"
    content = f"Your wallet withdrawal request has been received and will be processed within 5 business days."

    html_content = render_to_string(
        'EmailTemplate/basic_mail_template.html',
        {
            'subject': subject,
            'content': content,
            'year': datetime.now().year,
            'recipient_name': recipient_name,
            'solvify_logo_url': "https://solvifyhub.com/static/assets/solvify_logo.png",
        }
    )
    send_email_handler(subject, recipient_email, html_content)


def send_quote_mail(recipient_name, recipient_email):
    subject = "Wallet Withdrawal Request Received"
    content = f"Your wallet withdrawal request has been received and will be processed within 5 business days."

    html_content = render_to_string(
        'EmailTemplate/basic_mail_template.html',
        {
            'subject': subject,
            'content': content,
            'year': datetime.now().year,
            'recipient_name': recipient_name,
            'solvify_logo_url': "https://solvifyhub.com/static/assets/solvify_logo.png",
        }
    )
    send_email_handler(subject, recipient_email, html_content)
