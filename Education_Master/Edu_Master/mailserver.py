import os
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from . token import generate_token

# Email details
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_USER =  os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =  os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT =  os.environ.get('EMAIL_PORT')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



def send_mail_to_user(subject,message,to_email,name):
    form_email = EMAIL_HOST_USER
    Email_message = render_to_string('Admin_pannel/admin_email.html',
        {
       
            'name' : name,
            'message': message
        })
    send_mail(subject,Email_message,form_email,to_email,fail_silently=True)

def account_activation_link(email_subject,name,pk,to_email,requested_userID,request):
    current_site = get_current_site(request)
    form_email = EMAIL_HOST_USER
    email_messege = render_to_string('Admin_pannel/email_confirm.html',
        {
       
            'name' : name,
            'domain': current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(pk)),
            'token' : generate_token.make_token(requested_userID)
        })
    email = EmailMessage(
            email_subject,
            email_messege,
            form_email,
            to_email
        )
    email.fail_silently = True
    # email.send()

def send_email_with_attachment(subject,message,to_email,name,attached_file):
    form_email = EMAIL_HOST_USER
    Email_message = render_to_string('Admin_pannel/admin_email.html',
        {
       
            'name' : name,
            'message': message
        })
    mail = EmailMessage(subject,Email_message,form_email,to_email)
    mail.attach(attached_file.name,attached_file.read(),attached_file.content_type)
    mail.fail_silently = True
    mail.send()

