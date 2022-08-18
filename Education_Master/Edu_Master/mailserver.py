import os
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,send_mail

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
