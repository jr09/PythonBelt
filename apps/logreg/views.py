from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Userdb
# Create your views here.

def register(request):
    if request.method == 'POST':
        print 'im here'
        response = Userdb.objects.checkRegister(request.POST)
        if response[0] == False:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('first_app:index')
        request.session['user_name'] = response[1]['name']
        request.session['user_id'] = response[1]['id']
        request.session.modified = True
        return redirect('first_app:home')

def login(request):
    if request.method == 'POST':
        print 'im here'
        response = Userdb.objects.check_login(request.POST)
        print response
        if response[0] == False:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('first_app:index')
        request.session['user_name'] = response[1]['name']
        request.session['user_id'] = response[1]['id']
        request.session.modified = True
        return redirect('first_app:index')

def logout(request):
    if request.method == 'POST':
        request.session.pop('user_name')
        request.session.pop('user_id')
    return redirect('first_app:index')
