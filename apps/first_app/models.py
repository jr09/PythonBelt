from __future__ import unicode_literals
from ..logreg.models import Userdb
from django.db import models
from django.db.models import Q, Count
import datetime, time

# Create your models here.
class TravelPlanManager(models.Manager):
    def validate_plan(self, data, user_id):
        errors = []
        if len(data['destination']) == 0:
            errors.append('Destination Filed cannot be blank')
        if len(data['description']) == 0:
            errors.append('Description cannot be blank')
        if len(data['travel_from']) == 0 or len(data['travel_to']) == 0:
            errors.append('Dates cannot be blank')
            return [False, errors]
        curr_date = datetime.datetime.now()
        date_from = datetime.datetime.strptime(data['travel_from'], "%Y-%m-%d")
        date_to = datetime.datetime.strptime(data['travel_to'], "%Y-%m-%d")
        if curr_date > date_from:
            errors.append('Travel From date cannot be in the past')
        if date_from > date_to:
            errors.append('Travel To date cannot be in the past')
        if errors:
            return [False, errors]
        plan_created = TravelPlan.objects.create(creator=Userdb.objects.get(id=user_id), destination=data['destination'], description=data['description'], start_date=data['travel_from'], end_date=data['travel_to'])
        trip_created= Trip.objects.create(user=Userdb.objects.get(id=user_id), travel_plan=plan_created)
        return [True]

class TravelPlan(models.Model):
    creator = models.ForeignKey(Userdb, related_name='travel_user_reverse')
    destination = models.CharField(max_length=45)
    description = models.TextField()
    start_date = models.CharField(max_length=45)
    end_date = models.CharField(max_length=45)

    objects = TravelPlanManager()

    def __str__(self):
        return 'Creator: %s | Destination: %s' %(self.creator.name, self.destination)

class Trip(models.Model):
    user = models.ForeignKey(Userdb, related_name='trip_user_reverse')
    travel_plan = models.ForeignKey(TravelPlan, related_name='trip_travel_reverse')

    def __str__(self):
        return 'User: %s | Destination: %s' %(self.user.name, self.travel_plan.destination)


def getGoToHomeObject(user_id):
    print user_id
    user_present = []
    user_trips = Trip.objects.filter(user__id=user_id)
    other_plans = TravelPlan.objects.exclude(creator__id=user_id, trip_travel_reverse__user__id=user_id)
    for plan in other_plans:
        joined_users_list = plan.trip_travel_reverse.all().values_list('user_id', flat=True)
        print joined_users_list
        if user_id in joined_users_list:
            user_present.append(1)
        else:
            user_present.append(0)
    print user_present
    goToHOmeObject = {
        'user_trips': user_trips,
        'other_plans': zip(other_plans, user_present)
    }
    return goToHOmeObject

def getGoToDestinationObject(travelplan_id):
    travelplan_object = TravelPlan.objects.get(id=travelplan_id)
    users = Trip.objects.filter(travel_plan__id=travelplan_id).exclude(user__id=travelplan_object.creator.id)
    goToDestinationObject = {
        'travel_plan':travelplan_object,
        'users':users
    }
    return goToDestinationObject
