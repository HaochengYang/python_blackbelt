from __future__ import unicode_literals
from ..login.models import User
from django.db import models
from datetime import date, datetime
from dateutil.parser import parse as parse_date

class TripManager(models.Manager):
    def add_trip(self, request):
        errors = self.trip_validations(request)

        if errors:
            return (False, errors)

        user = User.objects.get(id=request.session['user']['user_id'])

        Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planner=user)

        return (True, errors)

    def join_trip(self, request, id):
        user = User.objects.get(id=request.session['user']['user_id'])

        trip = Trip.objects.get(id=id)

        trip.travelers.add(user)

    def trip_validations(self, request):
        errors = []
        print '*'*80
        print request.POST['start_date']
        print request.POST['end_date']
        print '*'*80

        try:
            start_date = parse_date(request.POST['start_date']).date()
            end_date = parse_date(request.POST['end_date']).date()
        except ValueError:
            errors.append('Please add a start and end date.')
            if not request.POST['destination']:
                errors.append('Please add a destination.')
            if not request.POST['description']:
                errors.append('Please add a description.')
            return errors
            
        if start_date < date.today():
            errors.append('Start date must be today or in the future.')
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
