#!/usr/bin/env python3
from mongoengine import *
from models import WalkingRoute
from json import dumps
from flask_login import UserMixin
from passlib.hash import sha256_crypt

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

    def verify_password(self, pass_input):
        '''
            verifies password
        '''
        return sha256_crypt.verify(pass_input, self.password)

    # initial password hashing takes place in api
