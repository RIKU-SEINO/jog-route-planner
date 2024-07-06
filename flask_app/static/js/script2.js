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

  $('#prefecture').prepend('<option value="" selected disabled>選択してください</option>');

  let map = L.map('mapid').setView([35.683969, 139.753326], 14);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // URLから取得したクエリパラメータ
  let startLatLngStr = getQueryParam('startLatLng');
  let goalLatLngStr = getQueryParam('goalLatLng');
  let targetLengthStr = getQueryParam('targetLength')
  let routeIndexStr = getQueryParam('routeIndex');

  // JSON文字列をJavaScriptオブジェクトにパース
  let startLatLng = JSON.parse(startLatLngStr);
  let goalLatLng = JSON.parse(goalLatLngStr);
  let targetLength = JSON.parse(targetLengthStr);
  let routeIndex = JSON.parse(routeIndexStr);

  //ルート情報を取得
  fetchRoute(startLatLng, goalLatLng, targetLength, routeIndex, map);
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

// URLからクエリパラメータを取得する関数
function getQueryParam(key) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(key);
}

function fetchRoute(startlatLng, goallatLng, targetLength, routeIndex, map) {
    fetch('/map',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            startlat: startlatLng.lat,
            startlng: startlatLng.lng,
            goallat: goallatLng.lat,
            goallng: goallatLng.lng,
            targetLength: targetLength
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }
        return response.json();
    }).then((routeData) => {
        let route = routeData["route"][routeIndex];
        let wayPointIndices = routeData["wayPointIndices"][routeIndex];
        let routeLatLng = route.map(coord => L.latLng(coord[1], coord[0]));
        let routeLength = Math.floor((routeData["routeLength"][routeIndex]/1e3) * 100) / 100
    
        //取得情報をelementに格納
        let distanceInputElement = document.getElementById("distance");
        distanceInputElement.value = routeLength;
        let routeLatLngInputElement = document.getElementById("route_latlng");
        routeLatLngInputElement.value = JSON.stringify(routeLatLng);
        let wayPointIndicesElement = document.getElementById("waypoint_indices");
        wayPointIndicesElement.value = JSON.stringify(wayPointIndices);
    
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
    })
}