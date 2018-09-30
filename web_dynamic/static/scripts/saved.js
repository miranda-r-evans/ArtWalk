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

let showRoute = function (directionsService, directionsDisplay, id) {
  $.ajax({
    url: 'http://127.0.0.1:5000/api/v1/walkingroutes/' + id,
    type: 'GET',
  }).done(function (data) {calculateAndDisplayRoute(directionsService, directionsDisplay, JSON.parse(data))})
}
