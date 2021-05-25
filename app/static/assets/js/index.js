console.log(mapdata)
console.log(sessionStorage)
var company  = String(company)

var company_no = company.slice(8);

var no = parseInt(company_no);


markers = [];
function initMap() {
  var india = {
    lat: 20.5937,
    lng: 78.9629,
  };
  map = new google.maps.Map(document.getElementById("map"), {
    center: india,
    zoom: 10,
    mapTypeId: "terrain", // roadmap, satellite, terrain, hybrid
  });
  infoWindow = new google.maps.InfoWindow();

  showStoreMarkers();
}

function showStoreMarkers() {
  var bounds = new google.maps.LatLngBounds();
  data = mapdata[no-1];

  data[company].forEach(function (city, index) {
    var latlng = new google.maps.LatLng(city.latitude, city.longitude);
    var name = city.Name;
    var count = city.Count;
    createMarker(latlng, name, count, index);
    bounds.extend(latlng);
  });
  map.fitBounds(bounds);
}

function createMarker(latlng, name, count, index) {
  var html = "<b>State : </b>" + name + "</b> <br/> <b>Tool Count: </b>" + count;
  var marker = new google.maps.Marker({
    map: map,
    position: latlng,
    label: `${index + 1}`,
  });
  google.maps.event.addListener(marker, "click", function () {
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
  });
  markers.push(marker);
}
