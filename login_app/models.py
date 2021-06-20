from django.db import models
import re
import bcrypt
from django.contrib import messages
import datetime
from datetime import datetime
from datetime import date


class UserManager(models.Manager):
    def registration_validation(self, postData):
        errors={}

        date=datetime.today()
        new_date=datetime(date.year, date.month, date.day)

        name_regex= re.compile(r'^[a-zA-Z]+$')
        email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['length_fn']="First name must be at least two characters."
        elif not name_regex.match(postData['first_name']):
            errors['regex_fn']="First name must only contain letters."
        if len(postData['last_name']) < 2:
            errors['length_ln']="Last name must be at least two characters."
        elif not name_regex.match(postData['last_name']):
            errors['regex_ln']="Last name must only contain letters."
        if not email_regex.match(postData['email']):
            errors['email']="Please enter a valid email."
        email_check= User.objects.filter(email=postData['email'])
        if len(email_check) > 0:
            errors['unique_email']="This email is already being used. Please enter a different email address."
        if len(postData['password']) < 8:
            errors['length_pwd']="Password must be at least 8 characters."
        elif postData['password'] != postData['password_conf']:
            errors['password']="Passwords must match."
        if len(postData['birthday']) == 0:
            errors['birthday']='Date of birth must be selected'
        elif datetime.strptime(postData['birthday'],'%Y-%m-%d') >= new_date:
            errors['birthday']="Birthday must be in the past"
    
        return errors

    def login_validation(self, postData):
        errors={}
        #Check if email is in database as registered user and return array of matches.
        login_user=User.objects.filter(email=postData['email'])
        #If filtering results in a match 
        if len(login_user) > 0:
            #Check to see if password entered matches password in database.
            if bcrypt.checkpw(postData['password'].encode(), login_user[0].password.encode()):
                #return messages.success(self, "Passwords matched.")
                pass
            else:
                errors['password']="Password does not match"
        else: 
            errors['email']="There is no user with that email"
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    birthday=models.DateField(default=date.today())
    email=models.EmailField(max_length=80) #unique=True
    password=models.CharField(max_length=60)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

# Create your models here.
