function gatherInput () {
  let params = {};
  params.origin = $('#origin').val();
  if ($('#radius').val() !== '') {
    params.radius = $('#radius').val();
  }
  return params;
}

function generateRoute (directionsService, directionsDisplay) {
  $('#loader').css('display', 'block');
  $.ajax({
    // sample route is for development purposes
    url: 'http://127.0.0.1:5000/api/v1/sampleroute',
    // url: 'http://127.0.0.1:5000/api/v1/generateRoute',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(gatherInput()),
    dataType: 'json',
    headers: {'Content-Type': 'application/json'}
  }).done(function (data) { calculateAndDisplayRoute(directionsService, directionsDisplay, data); });
}
