# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, regdata):

        flag = True
        error = []
        username_exist=True
        enter_flag = True


        try:
            preExist = self.get(username = regdata['username'])
        except self.model.DoesNotExist:
                username_exist = False
        if username_exist == False:

            if len(regdata['name']) < 1:
                error.append('Name is required.')
                flag=False

            elif len(regdata['name']) < 3:
                error.append("Your name must be at least 3 characters.")
                flag=False

            elif not (regdata['name']).replace(' ','').isalpha():
                error.append('Your name can only contain letters.')
                flag=False

        # ------------------------------------------------------------------------------
            if len(regdata['username']) < 1:
                error.append('Username is required.')
                flag=False

            elif len(regdata['username']) < 3:
                error.append("Your username must be at least 3 characters.")
                flag=False

        # ------------------------------------------------------------------------------

            if len(regdata['password']) < 1:
                error.append('Password is required.')
                flag=False

            elif len(regdata['password']) < 8:
                error.append('Your password must be greater than 8 characters.')
                flag=False
        # ------------------------------------------------------------------------------

            if len(regdata['cpassword']) < 1:
                error.append('Confirmation of password is required.')
                flag=False

            elif regdata['cpassword'] != regdata['password']:
                error.append('Confirmation of password must match password.')
                flag=False

            if flag == False:
                return error

            else:
                User.objects.create(name=regdata['name'], username=regdata['username'], password=regdata['password'], date_hired=regdata['datehired'])
                name = regdata['name']

                return {'name': name, 'action': "registered"}
        else:
            error.append('Username is already in database.')

    def login(self, logdata):

        lflag = True
        login_error = []
        exist_flag= True
        enter_flag=True

        if len(logdata['username']) == 0:
            login_error.append('Username is required.')
            lflag = False
            enter_flag=False
            exist_flag=False


        if len(logdata['login_password']) == 0:
            login_error.append('Password is required.')
            lflag= False
            enter_flag=False
            exist_flag=False


        if enter_flag==True:
            try:
                preExist = self.get(username = logdata['username'])
            except self.model.DoesNotExist:
                login_error.append('Username does not exist in database.')
                exist_flag = False
                lflag=False

        if exist_flag == True:

            if not logdata['username'] == preExist.username:
                login_error.append("Sorry, email does not exist or match our database")
                lflag = False
            elif not logdata['login_password'] == preExist.password:
                login_error.append("Password is incorrect.")
                lflag = False


        if lflag == False:
            return login_error

        else:
            lfirst_name = preExist.name
            l_id = preExist.id
            return {'name': lfirst_name, 'action': "logged in", 'user_id': l_id}


class User(models.Model):
    name = models.CharField(max_length=100)
    username= models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    name=models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name = 'items_added')
    date_added = models.DateField(auto_now_add=True)

class WishList(models.Model):
    user = models.ForeignKey(User, related_name='userfk')
    item = models.ForeignKey(Item, related_name='itemfk')
