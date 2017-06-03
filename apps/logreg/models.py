from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
import bcrypt, re

UNAME_REGEX = re.compile(r'([a-zA-Z0-9]{3,50})$')
NAME_REGEX = re.compile(r'([a-zA-Z\w\s]{3,50})$')
PWD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')

class UserdbManager(models.Manager):
    def checkRegister(self, data):
        errors = []
        if not NAME_REGEX.match(data['name']):
            errors.append('Name must be at least 3 characters long and not contain numbers or special characters')
        if not UNAME_REGEX.match(data['user_name']):
            errors.append('User Name must be at least 3 characters long')
        if not PWD_REGEX.match(data['pwd']):
            errors.append('Password must be at least 8 characters and must contain at least 1 uppercase letter, 1 digit and 1 special character')
        if data['pwd'] != data['conf_pwd']:
            errors.append('Confirm password does not match Password')
        if errors:
            return [False, errors]
        if Userdb.objects.filter(user_name=data['user_name']).first():
            errors.append('User name already in use, please use another email')
            return [False, errors]
        user_created = Userdb.objects.create(name=data['name'], user_name=data['user_name'], password=bcrypt.hashpw(data['pwd'].encode(), bcrypt.gensalt()))
        print user_created
        user_obj = {
            'name': user_created.name,
            'id': user_created.id
        }
        return [True, user_obj]

    def check_login(self, data):
        errors = []
        user_obj = Userdb.objects.filter(user_name=data['user_name']).first()
        if not user_obj:
            errors.append('Invalid user name or password')
        elif not bcrypt.checkpw(data['pwd'].encode(), user_obj.password.encode()):
            errors.append('Invalid user name or password')
        if errors:
            return [False, errors]
        user = {
            'name': user_obj.name,
            'id': user_obj.id
        }
        return [True, user]

class Userdb(models.Model):
    name = models.CharField(max_length=25)
    user_name = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects = UserdbManager()

    def __str__(self):
        return 'Name: %s | User Name: %s' %(self.name, self.user_name)
