# ArtWalk : Holberton School End-Of-Year Project
ArtWalk is a web application that allows users to generate, save, and recommend walking routes featuring murals, sculptures, and other landmarks anywhere in the world. It uses Google Maps for querying place data, displaying maps, and giving access to walking directions.

## Overview
ArtWalk has five front-end routes, used for randomly generating a walking route, creating a customized walking route of specific places, seeing popular walking routes, seeing saved walking routes, and logging in.

### Home
![screenshot of home](/images/home.png)
Generate A Route panel is used to randomly generate a route in a particular area. The advanced button allows for wanted and unwanted points. After a route is generated, the Open A Route panel pops up, which provides links to Google Maps. If the user is logged in, a panel to save or like the route pops up as well. The user can choose what name to give the route and what keywords to associate it with.

### Custom
![screenshot of custom](/images/custom.png)
Create A Route panel is used to create a route with specific places. The Open A Route and Like Or Save A Route panels work the same as in home.

### Recommended
![screenshot of recommended](/images/recommended.png)
The default behavior of recommended is to show the ten most popular routes, but the Search panel can be used to find routes based on a name or keyword. Sections for each route pop up, with a see button to see the route and like and save buttons if the user is logged in. Once a user sees a route, the Open A Route panel will pop up.

### My Routes
![screenshot of myroutes](/images/saved.png)
Myroutes works similarly to recommended, but does not have a search feature and shows only walking routes that a user has saved. The save button is not present here.

### Log In
![screenshot of login](/images/login.png)
The login page has a simple log in form that redirects the user to home once logged in.

## Technology Stack
The primary back-end technologies used are Python3 and MongoDB. The Python modules used are:
* flask
* flask-login
* flask-cors
* passlib
* requests
* mongoengine (+dependancies)

## Directions for Use
Download Python3, pip3, and MongoDB. Make sure that Python3 is in your path variable and MongoDB is configured properly.
```
$ sudo apt-get update
$ sudo apt-get install python3
...
$ sudo apt-get install -y mongodb-org
...
$ sudo apt-get install python3-pip
...
```
Next, pip3 the relevant modules.
```
$ pip3 install flask, flask-cors, flask-login, passlib, mongoengine
```
Currently, there are no server configuration directions. The web app should be available publicly. The API  app is used by the web app on the server and should not be available publicly, except for the routes */generateRoute, /customRoute, /routeSearch,* and */top10*. */sampleroute* is used for development purposes.

Lastly, a Google Maps API key is needed. Obtain an API key, create a file called `GoogleAPIKey.py` in the top-level directory, and inside create a variable called `APIKey` equal to the obtained API key.

## Possible Improvements
* Sign-up feature
* Server hosting and DNS set-up
* Prettier front-end
* Integrate liking and saving of new walking routes better to eliminate redundant walking routes from the database
* Have a more professional set-up for getting a secret key, rather than using urandom.
