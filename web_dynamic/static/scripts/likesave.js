$(document).ready(function() {
  $('#save_button').click(function() {
    $('#save_form').empty();
    $('#save_form').append(
      $('<form>', {'action': '/save', 'method': 'POST'}).append(
        $('<label>', {'for': 'route_name'}).text('name'),
        $('<br>'),
        $('<input>', {'type': 'text', 'name': 'name', 'value': $('#origin').val(), 'id': 'route_name'}),
        $('<br>'),
        $('<label>', {'for': 'route_keywords'}).text('keywords (separate by comma)'),
        $('<br>'),
        $('<input>', {'type': 'text', 'name': 'keywords', 'placeholder': 'Crab Sculpture,50 United Nations Plaza,30 minutes', 'id': 'route_keywords'}),
        $('<br>'),
        $('<input>', {'type': 'text', 'name': 'origin', 'value': currentRoute.origin, 'id': 'route_origin'}),
        $('<input>', {'type': 'text', 'name': 'waypoints', 'value': currentRoute.waypoints, 'id': 'route_waypoints'}),
        $('<input>', {'type': 'submit'})
      )
    );
  });
});
