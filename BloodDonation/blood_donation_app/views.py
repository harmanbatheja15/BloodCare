from django.shortcuts import render, redirect
from datetime import datetime
from .models import Contact, State, City, BloodBank
from account.models import Account
from django.contrib import messages, auth
from django.core.mail import EmailMessage, send_mail
import requests
from django.conf import settings
from django.contrib.auth.models import User
import psycopg2
import smtplib

# Create your views here.

def index(request):
    return render(request, "index.html")

# def about(request):
#     return render(request, "about.html")

def find_donor(request):

    s = State.objects.all().order_by('name')
    # blood_donors = Account.objects.all().order_by('state')
    blood_group_search = Account.objects.values_list('blood_group', flat=True).distinct()
    state_search = Account.objects.values_list('state', flat=True).distinct()
    city_search = Account.objects.values_list('city', flat=True).distinct()
    blood_group = request.GET.get('blood_group')
    state = request.GET.get('state')
    city = request.GET.get('city')
    blood_donors = Account.objects.filter(blood_group__iexact=blood_group, state=state, city=city)

    if 'blood_group' in request.GET:
        blood_group = request.GET['blood_group']
        if blood_group:
            blood_donors = blood_donors.filter(blood_group__iexact=blood_group)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            blood_donors = blood_donors.filter(state=state)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            blood_donors = blood_donors.filter(city=city)

    data = {
        's': s,
        'blood_donors': blood_donors,
        'blood_group_search': blood_group_search,
        'state_search': state_search,
        'city_search': city_search,
    }

    return render(request, "find_donor.html", data)

def load_cities(request):
    state_id = request.GET.get('state')
    city = City.objects.filter(state_id=state_id).order_by('name')
    data = {
        'city': city,
    }

    return render(request, "cities_dropdown_list_options.html", data)

def find_blood_banks(request):

    s = State.objects.all().order_by('name')

    state_search = BloodBank.objects.values_list('States', flat=True).distinct()

    state = request.GET.get('state')
    blood_banks = BloodBank.objects.filter(States__iexact=state).order_by("City")
    # blood_banks = BloodBank.objects.all().order_by('State')

    if 'States' in request.GET:
        States = request.GET['States']
        if States:
            blood_banks = blood_banks.filter(States=States)

    context = {
        'blood_banks': blood_banks,
        's': s,
        'state_search': state_search,
    }

    return render(request, "find_blood_banks.html", context)

def can_donate(request):
    return render(request, "can_donate.html")

def contribution(request):
    return render(request, "contribution.html")

def feedback(request):

    if(request.method == "POST"):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phone=phone, message=message, date=datetime.today())
        contact.save()
        messages.success(request, f'Thanks {name} for your feedback!')

        ''' send_mail(
            subject = "blood-care.org Feedback",
            message = f"Thanks {name} for your valuable feedback! We will get back to you soon.",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [email],
            fail_silently = True,
        ) '''

        ''' server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, email, f'Thanks {name} for your valuable feedback! We will get back to you soon.') '''

        return redirect('feedback')

    return render(request, "feedback.html")

def volunteers_technicalTeam(request):
    return render(request, "volunteers&technicalTeam.html")