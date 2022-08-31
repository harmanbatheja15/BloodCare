from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, AccountAuthenticationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import Account
from blood_donation_app.models import State, City
from django.core.mail import send_mail
from django.conf import settings
import smtplib

# Create your views here.

def load_cities(request):
    state_id = request.GET.get('state_id')
    city = City.objects.filter(state_id=state_id).order_by('name')
    
    data = {
        'city': city,
    }
    
    return render(request, 'account/cities_dropdown_list_options.html', data)

def registration_view(request):

    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            '''raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)'''

            """ send_mail(
                subject = "blood-care Registration",
                message = f"You are successfully registered in blood-care.org\nemail={email}\npassword={password}",
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently = False
            ) """

            """ server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, email, f'You are successfully registered in blood-care.org\nemail={email}\npassword={password}') """

            messages.success(request, "Your account has been created successfully!")
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("/")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            messages.success(request, "You are logged in successfully!")

            if user:
                login(request, user)
                return redirect("dashboard")

    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')

def dashboard_view(request):

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('dashboard')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    } 

    return render(request, 'account/dashboard.html', context)

class DeleteView(DeleteView):
    model = Account
    success_url = reverse_lazy('register')