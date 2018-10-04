function loadRoutes (data) {
  $('#savedroutes').empty();
  data.sort(function (a, b) { return b.likes - a.likes; });
  for (route of data) {
    $('#savedroutes').append(
      $('<div>', {'class': 'route', 'id': 'route.' + route['id']}).append(
        $('<h3>').text(route['name']),
        $('<h4>').text(route['likes']),
        $('<button>', {'class': 'seeroute', 'id': route['id']}).text('see'),
        $('<form>', {'action': '/existingwalk', 'method': 'POST'}).append(
          $('<input>', {'type': 'hidden', 'name': 'id', 'value': route['id']}),
          $('<button>', {'type': 'submit', 'name': 'action', 'value': 'like'}).text('like'),
          $('<button>', {'type': 'submit', 'name': 'action', 'value': 'save'}).text('save')
        )
      )
    );
  }
  initMap();
}

$(document).ready(function () {
  $.ajax({
    // top 10 is for production
    // url: 'http://0.0.0.0:5000/api/v1/top10/'
    url: 'http://0.0.0.0:5000/api/v1/walkingroutes/'
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
