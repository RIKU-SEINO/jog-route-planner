// URLからクエリパラメータを取得する関数
function getQueryParam(key) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(key);
}

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
  let routeLatLngStr = getQueryParam('routeLatLng');
  let wayPointIndicesStr = getQueryParam('wayPointIndices');
  let routeLengthStr = getQueryParam('routeLength');

  // JSON文字列をJavaScriptオブジェクトにパース
  let routeLatLng = JSON.parse(routeLatLngStr);
  let wayPointIndices = JSON.parse(wayPointIndicesStr);
  let routeLength = JSON.parse(routeLengthStr);

  let distanceInputElement = document.getElementById("distance");
  distanceInputElement.value = routeLength;
  let routeLatLngInputElement = document.getElementById("route_latlng");
  routeLatLngInputElement.value = routeLatLngStr;

  // 例：取得した情報をコンソールに出力して確認
  console.log('Route LatLng:', routeLatLng);
  console.log('Waypoint Indices:', wayPointIndices);
  console.log('Route Length:', routeLength);

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
                  $('#city').append('<option value="">選択してください</option>');
                  $.each(data, function(key, city) {
                      $('#city').append('<option value="' + city.id + '">' + city.name + '</option>');
                  });
              }
          });
      } else {
          $('#city').empty();
          $('#city').append('<option value="">選択してください</option>');
      }
  });
});