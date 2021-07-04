from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return render(request, "classmanager/index.html")


def login_view(request):
    return render(request, "classmanager/login.html")


def logout_view(request):
    return render(request, "classmanager/index.html")


def register(request):
    return render(request, "classmanager/register.html")


def contact_us(request):
    return render(request, "classmanager/contact_us.html")
