let showRoute = function (directionsService, directionsDisplay, id) {
  $('#loader').css('display', 'block');
  $.ajax({
    url: 'http://127.0.0.1:5000/api/v1/walkingroutes/' + id,
    type: 'GET'
  }).done(function (data) { calculateAndDisplayRoute(directionsService, directionsDisplay, JSON.parse(data)); });
};
