function initMap() {
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 6,
    center: {lat: 39.8283, lng: 98.5795}
  });
  directionsDisplay.setMap(map);

  document.getElementById('submit').addEventListener('click', function() {
  generateRoute(directionsService, directionsDisplay);
  });
}

let currentRoute = {"hello": "world"};

let gatherInput = function () {
  let params = {};
  params.origin = $('#origin').val();
  if ($('#radius').val() != '') {
    params.radius = $('#radius').val();
  }
  return params;
}

let generateRoute = function (directionsService, directionsDisplay) {
  $.ajax({
    url: 'http://127.0.0.1:5000/api/v1/sampleroute',
    //url: 'http://127.0.0.1:5000/api/v1/generateRoute',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(gatherInput()),
    dataType: 'json',
    headers: {'Content-Type': 'application/json'}
  }).done(function (data) {calculateAndDisplayRoute(directionsService, directionsDisplay, data)})
}

function calculateAndDisplayRoute(directionsService, directionsDisplay, data) {
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
