function initMap() {
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 6,
    center: {lat: 39.8283, lng: 98.5795}
  });
  directionsDisplay.setMap(map);

  $('.seeroute').click(function() {
  showRoute(directionsService, directionsDisplay, this.id);
  });
}

if (typeof currentRoute === 'undefined'){
  var currentRoute = {"hello": "world"};  
}

let showRoute = function (directionsService, directionsDisplay, id) {
  $.ajax({
    url: 'http://127.0.0.1:5000/api/v1/walkingroutes/' + id,
    type: 'GET',
  }).done(function (data) {calculateAndDisplayRoute(directionsService, directionsDisplay, data)})
}

function calculateAndDisplayRoute(directionsService, directionsDisplay, data) {
  data = JSON.parse(data)
  currentRoute = data;
  var waypts = []
  for (var i = 0; i < data.waypoints.length; i++) {
    waypts.push({
      location: {placeId: data.waypoints[i]},
      stopover: true
    });
  }
  directionsService.route({
    origin: {'placeId': data.origin},
    destination: {'placeId': data.origin},
    waypoints: waypts,
    optimizeWaypoints: true,
    travelMode: 'WALKING'
  }, function(response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    }
  );
}
