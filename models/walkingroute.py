#!/usr/bin/env python3
import requests
import random
from mongoengine import *
from models import APIKey
from json import dumps

connect('artwalk')


class WalkingRoute(Document):
    '''
        walking route class
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
    def findClustering(points):
        '''
            finds optimal walk by identifying clusters
        '''
        for x in points:
            x['clustering_score'] = 0
            for y in points:
                x['clustering_score'] += abs(x['geometry']['location']['lat'] - y['geometry']['location']['lat'])
                x['clustering_score'] += abs(x['geometry']['location']['lng'] - y['geometry']['location']['lng'])
        points.sort(key = lambda z:z['clustering_score'], reverse=True)
        return points

    @staticmethod
    def generateRoute(origin, optimize=False, radius=1, wantedPoints='', unwantedPoints=''):
        '''
            generate a route around an origin point
        '''
        wantedPoints = wantedPoints.split(',')
        unwantedPoints = unwantedPoints.split(',')
        originLocation = WalkingRoute.getLocation(origin)
        placeTypes = ['sculpture', 'mural', 'fountain']

        # concatenate all landmarks around origin into one list
        placeList = []
        for keyword in placeTypes:
            try:
                ## '&rankby=prominence' doesn't place nice with radius, but should be investigated more
                placeList.extend(requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyAhHMgVekplsXZxpqkkwpctPH3fFBe1Ilc&location=' + str(originLocation['geometry']['location']['lat']) + ',' + str(originLocation['geometry']['location']['lng']) + '&radius=' + str(int(radius) * 1609) + '&keyword=' + keyword).json()['results'])
            except (IndexError, KeyError):
                return None
        ## removing duplicate elements from placeList is an option, but will take additional computation with little benefit

        # add wanted places and choose more places randomly from placeList
        waypoints = []
        for name in wantedPoints:
            location = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyAhHMgVekplsXZxpqkkwpctPH3fFBe1Ilc&location=' + str(originLocation['geometry']['location']['lat']) + ',' + str(originLocation['geometry']['location']['lng']) + '&radius=' + str(16090) + '&keyword=' + name).json()['results'][0]
            if location is not None:
                waypoints.append(location['place_id'])

        if optimize is True:
            placeList = WalkingRoute.findClustering(placeList)

        i = len(waypoints)
        while i < 23:
            if len(placeList) == 0:
                break

            if optimize is True:
                randPoint = placeList.pop()
            else:
                randPoint = placeList.pop(random.choice(range(len(placeList))))

            if randPoint['name'] not in wantedPoints and randPoint['name'] not in ['unwantedPoints'] and randPoint.get('price_level') is None:
                waypoints.append(randPoint['place_id'])
                i += 1

        return {'origin': originLocation['place_id'], 'waypoints': waypoints}

    @staticmethod
    def customRoute(origin, waypoints):
        '''
            create custom route
        '''
        originLocation = WalkingRoute.getLocation(origin)
        waypointsLocations = [requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyAhHMgVekplsXZxpqkkwpctPH3fFBe1Ilc&location=' + str(originLocation['geometry']['location']['lat']) + ',' + str(originLocation['geometry']['location']['lng']) + '&radius=' + str(16090) + '&keyword=' + point.replace(' ', '%20')).json()['results'][0]['place_id'] for point in waypoints.split(',')]
        return {'origin': originLocation['place_id'], 'waypoints': waypointsLocations}
