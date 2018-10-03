var currentRoute = {'hello': 'world'};

// this function is required by Google Maps JS API for rendering the map
function initMap () {
  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer();
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: {lat: 39.8283, lng: -98.5795}
  });
  directionsDisplay.setMap(map);

  // each extra script will have its respective functions executed, while ones from other files are ignored
  $('#random').click(function () {
    try {
      generateRoute(directionsService, directionsDisplay);
    } catch (ReferenceError) {

    }
  });

  $('#optimal').click(function () {
    try {
      generateRouteOptimal(directionsService, directionsDisplay);
    } catch (ReferenceError) {

    }
  });

  $('#submit_route').click(function () {
    try {
      customRoute(directionsService, directionsDisplay);
    } catch (ReferenceError) {

    }
  });

  $('.seeroute').click(function () {
    try {
      showRoute(directionsService, directionsDisplay, this.id);
    } catch (ReferenceError) {

    }
  });
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
      // current route is used to open a route in Google Maps
      // the waypoints should be in order
      currentRoute = {};
      currentRoute.origin = data.origin;
      currentRoute.waypoints = [];
      for (let i = 1; i < response['geocoded_waypoints'].length - 1; i++) {
        currentRoute.waypoints.push(response['geocoded_waypoints'][i]['place_id']);
      }

      // three legs are used because the Google Maps JS Api can do 23 waypoints,
      // but Google Maps itself can only do 9 points
      let totalRoute = currentRoute.waypoints.slice();
      totalRoute.push(currentRoute.origin);
      totalRoute.unshift(currentRoute.origin);
      let leg1 = totalRoute.slice(0, 9);
      let leg2 = totalRoute.slice(8, 17);
      let leg3 = totalRoute.slice(16, 24);

      if (leg1.length > 0) {
        let link = 'https://www.google.com/maps/dir/?api=1&origin=a&destination=a&travelmode=walking&waypoints=' + 'a%7C'.repeat(leg1.length - 3) + 'a&origin_place_id=' + leg1.shift() + '&destination_place_id=' + leg1.pop() + '&waypoint_place_ids=' + leg1.join('%7C');
        $('#googlemaps1').attr('href', link);
      } else {
        $('#googlemaps1').css('display', 'none');
        window.alert('There was a problem generating the route');
        return;
      }

      if (leg2.length > 1) {
        link = 'https://www.google.com/maps/dir/?api=1&origin=a&destination=a&travelmode=walking&waypoints=' + 'a%7C'.repeat(leg2.length - 3) + 'a&origin_place_id=' + leg2.shift() + '&destination_place_id=' + leg2.pop() + '&waypoint_place_ids=' + leg2.join('%7C');
        $('#googlemaps2').attr('href', link);
      } else {
        $('#googlemaps2').css('display', 'none');
      }

      if (leg3.length > 1) {
        link = 'https://www.google.com/maps/dir/?api=1&origin=a&destination=a&travelmode=walking&waypoints=' + 'a%7C'.repeat(leg3.length - 3) + 'a&origin_place_id=' + leg3.shift() + '&destination_place_id=' + leg3.pop() + '&waypoint_place_ids=' + leg3.join('%7C');
        $('#googlemaps3').attr('href', link);
      } else {
        $('#googlemaps3').css('display', 'none');
      }

      directionsDisplay.setDirections(response);
      $('#loader').css('display', 'none');
      $('.likesave').css('display', 'block');
      $('.open').css('display', 'block');
      $('#route_origin').val(currentRoute.origin);
      $('#route_waypoints').val(currentRoute.waypoints);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  }
  );
}
