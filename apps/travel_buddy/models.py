from __future__ import unicode_literals
from ..login.models import User
from django.db import models
from datetime import date, datetime
from dateutil.parser import parse as parse_date

class TripManager(models.Manager):
    def add_trip(self, request):
        errors = self.trip_validations(request)

        if errors:
            return errors

        user = User.objects.get(id=request.session['user']['user_id'])

        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planner=user)

        return errors

    def join_trip(self, request, id):
        user = User.objects.get(id=request.session['user']['user_id'])

        trip = Trip.objects.get(id=id)

        trip.travelers.add(user)

    def trip_validations(self, request):
        errors = []
        
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date:
            start_date = parse_date(start_date).date()
            if start_date < date.today():
                errors.append('Start date must be today or in the future.')
        else:
            errors.append('Please add a start date.')

        if end_date:
            end_date = parse_date(end_date).date()
            if end_date < date.today():
                errors.append('End date must be today or in the future.')
        else:
            errors.append('Please add an end date.')

        if start_date and end_date:
            if start_date > end_date:
                errors.append('End date must be after or the same as start date.')
            
        if not request.POST['destination']:
            errors.append('Please add a destination.')
        if not request.POST['description']:
            errors.append('Please add a description.')

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length = 50)
    description = models.CharField(max_length = 140)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    planner = models.ForeignKey(User, related_name='trip')
    travelers = models.ManyToManyField(User, related_name='trips')

    objects = TripManager()
