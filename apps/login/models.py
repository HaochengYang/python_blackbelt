from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bcrypt

class UserManager(models.Manager):
    def validate_reg(self, request):
        errors = self.validate_inputs(request)

        if errors:
            return (False, errors)

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = self.create(name=request.POST['name'], username=request.POST['username'], password=pw_hash)

        return (True, user)

    def validate_login(self, request):
        try:
            user = User.objects.get(username=request.POST['username'])
            password = request.POST['password'].encode()
            if bcrypt.checkpw(password, user.password.encode()):
                return (True, user)

        except ObjectDoesNotExist:
            pass

        return (False, ["Invalid login."])

    def validate_inputs(self, request):
        errors = []

        if not request.POST['name']:
            errors.append('First name cannot be blank.')
        elif len(request.POST['name']) < 3:
            errors.append('Name must be more than 3 characters.')
        if not request.POST['username']:
            errors.append('Please enter a username.')
        if len(request.POST['password']) < 8:
            errors.append('Password must be at least 8 characters.')
        if request.POST['password'] != request.POST['confirm']:
            errors.append('Password and password confirm must match.')

        return errors

class User(models.Model):
    name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
