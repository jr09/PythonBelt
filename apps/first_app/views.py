from django.shortcuts import render, redirect
from ..logreg.models import Userdb


# Create your views here.

#first_app views

def index(request):
    if 'user_name' in request.session:
        return redirect('first_app:home')
    else:
        return render(request, 'first_app/index.html')

def home(request):
    return render(request, 'first_app/home.html')
