#!/usr/bin/env python3
import requests
import random
from mongoengine import *
from models import APIKey
from json import dumps

connect('artwalk')


class WalkingRoute(Document):
    '''
        route class
    '''
    name = StringField()
    origin = StringField(required=True)
    waypoints = ListField(StringField(), required=True)
    keywords = ListField(StringField())
    likes = IntField(required=True)


    def to_dict(self):
        '''
            dict representation of route
            can cause error if object is not already saved
        '''
        return {'id': str(self.id), 'name': self.name, 'origin': self.origin, 'waypoints': self.waypoints, 'keywords': self.keywords, 'likes': self.likes}


    def __str__(self):
        '''
            string version of object
        '''
        return dumps(self.to_dict())


    @staticmethod
    def find(id):
        '''
            finds a walkingroute instance
        '''
        try:
            return WalkingRoute.objects.get(id=id)
        except IndexError:
            return None


    @staticmethod
    def getLocation(name):
        '''
            get data of a place from a string
        '''
        try:
            ## taking out ['geometry']['location']
            return requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=' + APIKey + '&input=' + name.replace(' ', '%20') + '&inputtype=textquery&fields=place_id,geometry').json()['candidates'][0]
        except (IndexError, KeyError):
            return None


    @staticmethod
    def generateRoute(origin, radius=1, wantedPoints=[], unwantedPoints=[]):
        '''
            generate a route around an origin point
        '''
        originLocation = WalkingRoute.getLocation(origin)
        placeTypes = ['sculpture', 'mural', 'fountain']

        # concatenate all landmarks around origin into one list
        placeList = []
        for keyword in placeTypes:
            try:
                ## '&rankby=prominence' doesn't place nice with radius, but should be investigated more
                placeList.extend(requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyAhHMgVekplsXZxpqkkwpctPH3fFBe1Ilc&location=' + str(originLocation['geometry']['location']['lat']) + ',' + str(originLocation['geometry']['location']['lng']) + '&radius=' + str(radius * 1609) + '&keyword=' + keyword).json()['results'])
            except (IndexError, KeyError):
                return None
        ## removing duplicate elements from placeList is an option, but will take additional computation with little benefit

        # add wanted places and choose more places randomly from placeList
        waypoints = []
        for name in wantedPoints:
            location = WalkingRoute.getLocation(name)
            if location is not None:
                waypoints.append(location['place_id'])
        for i in range(len(waypoints), 23):
            if len(placeList) == 0:
                break
            randPoint = placeList.pop(random.choice(range(len(placeList))))
            if randPoint['name'] not in wantedPoints and randPoint['name'] not in ['unwantedPoints']:
                waypoints.append(randPoint['place_id'])

        return {'origin': originLocation['place_id'], 'waypoints': waypoints}

    @staticmethod
    def customRoute(origin, waypoints):
        '''
            create custom route
        '''
        originLocation = WalkingRoute.getLocation(origin)
        waypointsLocations = [requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyAhHMgVekplsXZxpqkkwpctPH3fFBe1Ilc&location=' + str(originLocation['geometry']['location']['lat']) + ',' + str(originLocation['geometry']['location']['lng']) + '&radius=' + str(16090) + '&keyword=' + point.replace(' ', '%20')).json()['results'][0]['place_id'] for point in waypoints.split(',')]
        return {'origin': originLocation['place_id'], 'waypoints': waypointsLocations}
