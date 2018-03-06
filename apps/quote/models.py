# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = []
        if len(postData['name']) < 2:
            errors.append("Name should be more than 2 characters")
        if len(postData['alias']) < 2:
            errors.append("alias too short")
        if len(postData['email']) < 5:
            errors.append("Enter valid email")
        if len(postData['password']) < 6:
            errors.append("Password should be more than 6 characters")
        if postData['confirmpassword'] != postData['password']:
            errors.append("Passwords do not match")
        if len(errors) == 0:
            return True,
        if len(errors) >0:
            return False, errors
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    favorite = models.ManyToManyField('Quote', related_name="favorite", default= None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    #def __str__(self):
        #return self.name

class QuoteManager(models.Manager):
    def validateQuote(self, postData):
        errors = []
        if len(postData['quote']) < 10:
            errors.append("Message should be more than 10 characters")
        if len(postData['quotedby']) < 3:
            errors.append("Quoted by should be more than 2 characters")
        if len(errors) == 0:
            return True,
        if len(errors) >0:
            return False, errors
        return errors

class Quote(models.Model):
    quote = models.TextField(max_length=100)
    quotedby = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="userquotes")
    objects = QuoteManager()
