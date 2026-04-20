from django.shortcuts import render, redirect

# Create your views here.
def register(request):
    from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import RegistrationForm
from .models import Account

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            email        = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password     = form.cleaned_data['password']

            # Auto generate username from email
            username = email.split('@')[0]

            # Check if email already exists
            if Account.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists. Please login instead.')
                return redirect('register')

            # Check if username already exists
            if Account.objects.filter(username=username).exists():
                username = f'{username}_{Account.objects.count()}'

            user = Account.objects.create_user(
                first_name = first_name,
                last_name  = last_name,
                email      = email,
                username   = username,
                password   = password,
            )
            user.phone_number = phone_number
            user.save()

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        else:
            #Show form validation errors to user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)  # ← fixed path

def login(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('shop')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
