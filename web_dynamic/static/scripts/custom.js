function initMap () {
  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer();
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 39.8283, lng: -98.5795}
  });
  directionsDisplay.setMap(map);

  document.getElementById('submit_route').addEventListener('click', function () {
    customRoute(directionsService, directionsDisplay);
  });
}

let gatherInput = function () {
  let params = {};
  params.origin = $('#origin').val();
  params.waypoints = $('#waypoints').val();
  return params;
};

let customRoute = function (directionsService, directionsDisplay) {
  $('#loader').css('display', 'block')
  $.ajax({
    url: 'http://127.0.0.1:5000/api/v1/customRoute',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(gatherInput()),
    dataType: 'json',
    headers: {'Content-Type': 'application/json'}
  }).done(function (data) { calculateAndDisplayRoute(directionsService, directionsDisplay, data); });
};
