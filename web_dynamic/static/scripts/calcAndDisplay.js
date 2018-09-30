if (typeof currentRoute === 'undefined') {
  var currentRoute = {'hello': 'world'};
}

function calculateAndDisplayRoute (directionsService, directionsDisplay, data) {
  var waypts = [];
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
  }, function (response, status) {
    if (status === 'OK') {
      currentRoute = {};
      currentRoute.origin = data.origin;
      currentRoute.waypoints = [];
      for (let i = 1; i < response['geocoded_waypoints'].length - 1; i++) {
        currentRoute.waypoints.push(response['geocoded_waypoints'][i]['place_id']);
      }

      let totalRoute = currentRoute.waypoints.slice();
      totalRoute.push(currentRoute.origin);
      totalRoute.unshift(currentRoute.origin);
      let leg1 = totalRoute.slice(0, 9);
      let leg2 = totalRoute.slice(9, 18);
      let leg3 = totalRoute.slice(18, 24);

      let link = 'https://www.google.com/maps/dir/?api=1&origin=a&destination=a&travelmode=walking&waypoints=' + 'a%7C'.repeat(leg1.length - 3) + 'a&origin_place_id=' + leg1.shift() + '&destination_place_id=' + leg1.pop() + '&waypoint_place_ids=' + leg1.join('%7C');
      $('#googlemaps1').attr('href', link);

      if (leg2.length !== 0) {
        link = 'https://www.google.com/maps/dir/?api=1&origin=a&destination=a&travelmode=walking&waypoints=' + 'a%7C'.repeat(leg2.length - 3) + 'a&origin_place_id=' + leg2.shift() + '&destination_place_id=' + leg2.pop() + '&waypoint_place_ids=' + leg2.join('%7C');
        $('#googlemaps2').attr('href', link);
      } else {
        $('#googlemaps2').attr('href', '');
      }

      if (leg3.length !== 0) {
        link = 'https://www.google.com/maps/dir/?api=1&origin=a&destination=a&travelmode=walking&waypoints=' + 'a%7C'.repeat(leg3.length - 3) + 'a&origin_place_id=' + leg3.shift() + '&destination_place_id=' + leg3.pop() + '&waypoint_place_ids=' + leg3.join('%7C');
        $('#googlemaps3').attr('href', link);
      } else {
        $('#googlemaps3').attr('href', '');
      }

      directionsDisplay.setDirections(response);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  }
  );
}
