from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
import bcrypt, re

EMAIL_REGEX = re.compile(r'[a-zA-z0-9.-_+]+@[a-zA-Z0-9.-_+]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'([a-zA-Z]{2,50})$')
PWD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

class UserdbManager(models.Manager):
    def checkRegister(self, data):
        errors = []
        if not NAME_REGEX.match(data['fname']):
            errors.append('First Name must be at least 2 characters long')
        if not NAME_REGEX.match(data['lname']):
            errors.append('Last Name must be at least 2 characters long')
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Please enter a valid email')
        if not PWD_REGEX.match(data['pwd']):
            errors.append('Password must be at least 8 characters and must contain at least 1 uppercase letter, 1 digit and 1 special character')
        if data['pwd'] != data['conf_pwd']:
            errors.append('Confirm password does not match Password')
        if errors:
            return [False, errors]
        if Userdb.objects.filter(email=data['email']).first():
            errors.append('Email already in use, please use another email')
            return [False, errors]
        user_created = Userdb.objects.create(fname=data['fname'], lname=data['lname'], email=data['email'], password=bcrypt.hashpw(data['pwd'].encode(), bcrypt.gensalt()))
        print user_created
        user_obj = {
            'name': user_created.fname,
            'id': user_created.id
        }
        return [True, user_obj]

    def check_login(self, data):
        errors = []
        user_obj = Userdb.objects.filter(email=data['email']).first()
        if not user_obj:
            errors.append('Invalid email or password')
        elif not bcrypt.checkpw(data['pwd'].encode(), user_obj.password.encode()):
            errors.append('Invalid email or password')
        if errors:
            return [False, errors]
        user = {
            'name': user_obj.fname,
            'id': user_obj.id
        }
        return [True, user]

class Userdb(models.Model):
    fname = models.CharField(max_length=25)
    lname = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects = UserdbManager()

    def __str__(self):
        return 'First Name: %s | Last Name: %s | Email: %s' %(self.fname, self.lname, self.email)
