function loadRoutes (data) {
  $('#savedroutes').empty();
  for (route of data) {
    $('#savedroutes').append(
      $('<div>', {'class': 'route', 'id': 'route.' + route['id']}).append(
        $('<h3>').text(route['name']),
        $('<h4>').text(route['likes']),
        $('<button>', {'class': 'seeroute', 'id': route['id']}).text('see'),
        $('<form>', {'action': '/saveRecommend', 'method': 'POST'}).append(
          $('<input>', {'type': 'hidden', 'name': 'id', 'value': route['id'], 'class': 'save_field'}),
          $('<button>', {'type': 'submit'}).text('save')
        )
      )
    );
  }
  initMap();
}

$(document).ready(function () {
  $.ajax({
    url: 'http://0.0.0.0:5000/api/v1/top10/'
  }).done(function (data) {
    loadRoutes(data);
  });

  $('#searchbutton').click(function () {
    $.ajax({
      url: 'http://0.0.0.0:5000/api/v1/routeSearch/' + $('#searchbar').val() + '/'
    }).done(function (data) {
      loadRoutes(data);
    });
  });
});
