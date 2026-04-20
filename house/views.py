from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name')
        email   = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        #Validate all fields
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('contact')

        #Send email to your inbox
        try:
            send_mail(
                subject      = f'[Microoo Contact] {subject}',
                message      = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email   = settings.EMAIL_HOST_USER,
                recipient_list = [settings.EMAIL_HOST_USER],
                fail_silently = False,
            )
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please try again.')

        return redirect('contact')

    return render(request, 'contact.html')
    return render(request, 'contact.html')