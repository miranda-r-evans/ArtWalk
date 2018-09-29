#!/usr/bin/env python3
from mongoengine import *
from models import WalkingRoute
from json import dumps
from flask_login import UserMixin

connect('artwalk')


class User(UserMixin, Document):
    '''
        user class
    '''
    name = StringField()
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    ## saving ids is easier than using a reference field, but could cause a bug if object is deleted and id is recycled
    ## syntax looks like ListField(ReferenceField(WalkingRoute, reverse_delete_rule=NULLIFY))
    liked = ListField(StringField())
    saved = ListField(StringField())


    def to_dict(self):
        '''
            dict representation of user
            can cause error if object is not already saved
        '''
        return {'id': str(self.id), 'name': self.name, 'email': self.email, 'liked': self.liked, 'saved': self.saved}


    def __str__(self):
        '''
            string version of object
        '''
        return dumps(self.to_dict())


    @staticmethod
    def find(id):
        '''
            finds a user instance
        '''
        try:
            return User.objects.get(id=id)
        except IndexError:
            return None


    # TODO: add password hashing
