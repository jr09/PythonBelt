from django.shortcuts import render, redirect
from ..logreg.models import Userdb
from django.contrib import messages
from .models import TravelPlan, Trip, getGoToHomeObject, getGoToDestinationObject


# Create your views here.

#first_app views

def index(request):
    if 'user_name' in request.session:
        return redirect('first_app:home')
    else:
        return render(request, 'first_app/index.html')

def home(request):
    gotTOHomeObject = getGoToHomeObject(request.session['user_id'])
    context = {
     'name': request.session['name'],
     'user_id': request.session['user_id'],
     'user_trips': gotTOHomeObject['user_trips'],
     'other_plans': gotTOHomeObject['other_plans']
    }
    return render(request, 'first_app/home.html', context)

def goToDestination(request, travelplan_id):
    goToDestinationObject = getGoToDestinationObject(travelplan_id)
    context = {
         'name': request.session['name'],
         'user_id': request.session['user_id'],
         'travel_plan':goToDestinationObject['travel_plan'],
         'users':goToDestinationObject['users']
    }
    return render(request, 'first_app/destination.html', context)

def add(request):
    context = {
         'name': request.session['name'],
         'user_id': request.session['user_id'],
    }
    return render(request, 'first_app/add.html', context)


def addplan(request, user_id):
    if request.method == 'POST':
        response = TravelPlan.objects.validate_plan(request.POST, user_id)
        if response[0] == False:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error)
            return redirect('first_app:add')
        elif response[0] == True:
            return redirect('first_app:home')

def join(request, travelplan_id):
    if request.method == 'POST':
        user_id = request.session['user_id']
        trip_create = Trip.objects.create(user=Userdb.objects.get(id=user_id), travel_plan=TravelPlan.objects.get(id=travelplan_id))
    return redirect('first_app:home')
