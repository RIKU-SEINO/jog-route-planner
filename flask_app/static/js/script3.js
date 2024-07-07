let startIcon = L.divIcon({
  html: `<div style="background-color: #3085d6; height:30px; width:30px; border-radius: 50%; padding: 6px 7px 10px 9px; display: block;">
          <i class="fa-solid fa-s fa-xl" style="color: #fff; width: 58%;"></i>
      </div>`,
  iconSize: [24, 24], // アイコンのサイズ
  iconAnchor: [12, 12],
});

let goalIcon = L.divIcon({
  html: `<div style="background-color: green; height:30px; width:30px; border-radius: 50%; padding: 6px 7px 10px 7px; display: block;">
          <i class="fa-solid fa-g fa-xl" style="color: #fff; width: 78%;"></i>
      </div>`,
  iconSize: [24, 24], // アイコンのサイズ
  iconAnchor: [12, 12],
});

// ページ読み込み時の処理
window.onload = function() {
  
  console.log("onload!!");

  let map = L.map('mapid').setView([35.683969, 139.753326], 14);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  let routeLatLng = JSON.parse(document.getElementById('course-info-route').getAttribute('data-course'));
  let wayPointIndices = JSON.parse(document.getElementById('course-info-waypoint_indices').getAttribute('data-course'));
  
  $('#prefecture').prepend('<option value="" selected disabled>選択してください</option>');
  //ルート情報を取得
  fetchRoute(routeLatLng, wayPointIndices, map);
};

$(document).ready(function() {
    $('#prefecture').change(function() {
        var prefectureId = $(this).val();
        if (prefectureId) {
            $.ajax({
                url: '/courses/get_cities',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ prefecture_id: prefectureId }),
                success: function(data) {
                    $('#city').empty();
                    $('#city').append('<option value="">全域</option>');
                    $.each(data, function(key, city) {
                        $('#city').append('<option value="' + city.id + '">' + city.name + '</option>');
                    });
                }
            });
        } else {
            $('#city').empty();
            $('#city').append('<option value="">全域</option>');
        }
    });
  });

function fetchRoute(routeLatLng, wayPointIndices, map) {
    let routePolyline = L.polyline(routeLatLng, { color: 'red' })
    routePolyline.addTo(map);
    map.fitBounds(routePolyline.getBounds().pad(0.1));
    
    let startMarker = L.marker(routeLatLng[0], {icon:startIcon}).addTo(map); 
    let goalMarker = L.marker(routeLatLng[routeLatLng.length-1], {icon:goalIcon}).addTo(map); 
    var wayPointCnt = 0;
    for (var i = 0; i < routeLatLng.length; i++) {
        if (wayPointIndices.includes(i) && !(i == 0) && !(i == routeLatLng.length-1)) {
            wayPointCnt = wayPointCnt + 1;
            let wayPointIcon = L.divIcon({
                html: `<div style="background-color: white; height:20px; width:20px; border: 1px solid #000; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-family: 'Century Gothic',sans-serif; font-weight: 900;">
                        <span>`+wayPointCnt+`<\span>
                    </div>`,
                iconSize: [15, 15], // アイコンのサイズ
                iconAnchor: [7, 7],
            });  
            let waypointMarker = L.marker(routeLatLng[i], {icon: wayPointIcon}).addTo(map);
        }
    }
}

function handleDownload() {
    let routeFilename = document.getElementById("download").getAttribute("download");
    let routeLatLng = JSON.parse(document.getElementById('course-info-route').getAttribute('data-course'));

    let content = generateRouteKML(routeLatLng);
    let blob = new Blob([ content ], {type: 'application/vnd.google-earth.kml+xml'});

    if (window.navigator.msSaveBlob) { 
        window.navigator.msSaveBlob(blob, routeFilename); 

        // msSaveOrOpenBlobの場合はファイルを保存せずに開ける
        window.navigator.msSaveOrOpenBlob(blob, routeFilename); 
    } else {
        document.getElementById("download").href = window.URL.createObjectURL(blob);
    }
}

function generateRouteKML(routeLatLng) {
    var kmlString = '<?xml version="1.0" encoding="UTF-8"?>';
    kmlString += '<kml xmlns="http://www.opengis.net/kml/2.2">';
    kmlString += '<Document>';
    kmlString += '<name>Route.kml</name>';
    kmlString += '<Placemark>';
    kmlString += '<name>Route</name>';
    kmlString += '<LineString>';
    kmlString += '<coordinates>';

    // 緯度経度データをKMLに追加
    routeLatLng.forEach(function(point) {
        kmlString += point.lng + ',' + point.lat + ' ';
    });

    kmlString += '</coordinates>';
    kmlString += '</LineString>';
    kmlString += '</Placemark>';
    kmlString += '</Document>';
    kmlString += '</kml>';

    return kmlString;
} 