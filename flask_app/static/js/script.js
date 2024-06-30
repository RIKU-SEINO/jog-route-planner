const map = L.map('map').setView([35.683969, 139.753326], 14);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

map.zoomControl.setPosition('bottomleft');

let routeSearchButton = document.getElementById("searchBtn")

let startMarker = null;
let goalMarker = null;
let startlatLng = null;
let goallatLng = null;

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

map.on('click', function(e) {
    let latLng = e.latlng;
    showChoicePopup().then((choice) => {
        if (choice == "start") {
            if (startMarker){
                map.removeLayer(startMarker);
            }
            startMarker = L.marker(latLng, {icon:startIcon}).addTo(map);
            startlatLng = latLng;
            reverseGeoCoder(startlatLng)
                .then(data => {
                    const address = data.address;
                    document.getElementById("input-start-point").value = address;
                })
                .catch(error => console.error(error));
        } else if (choice == "goal") {
            if (goalMarker){
                map.removeLayer(goalMarker);
            }
            goalMarker = L.marker(latLng, {icon:goalIcon}).addTo(map);
            goallatLng = latLng;
            reverseGeoCoder(goallatLng)
                .then(data => {
                    const address = data.address;
                    document.getElementById("input-goal-point").value = address;
                })
                .catch(error => console.error(error));
        } else if (choice == "cancel") {
            // キャンセル時の処理
        }
    });
})

let startInputElement = document.getElementById('input-start-point');
let goalInputElement = document.getElementById('input-goal-point');
setupAutocomplete(startInputElement);
setupAutocomplete(goalInputElement);

const deleteWaypointBtns = document.getElementsByClassName('delete-waypoint');
for (var i=0; i<deleteWaypointBtns.length; i++){
    let deleteWaypointBtn = deleteWaypointBtns[i];
    deletePoint(deleteWaypointBtn);
}

var _routeData = null;
let routeIndex = 0;
routeSearchButton.addEventListener('click', function() {
    clearAllMarker();
    clearAllPolyline();
    if ((startMarker) && (goalMarker)){
        fetchRoute(startlatLng, goallatLng)
    }else{
        let alertMessage = "が登録されていません。";
        let lackedItem;
        if ((!startMarker) && (!goalMarker)){
            lackedItem = "スタート地点とゴール地点"
        }else if(!startMarker) {
            lackedItem = "スタート地点";
        }else{
            lackedItem = "ゴール地点";
        }
        alertMessage = lackedItem + alertMessage;
        Swal.fire({
            text: alertMessage,
            icon: "error",
            backdrop: false
        })
    }
})
let registerCourseLink = document.getElementById('post-course-link');
let showPrevRouteButton = document.getElementById('prev-course');
let showNextRouteButton = document.getElementById('next-course');
let routeTitleElem = document.querySelector('.course-title');
let routeLengthElem = document.querySelector('.course-distance');
showPrevRouteButton.addEventListener('click',function () {
    if (_routeIndex > 0) {
        clearAllMarker();
        clearAllPolyline();
        _routeIndex--;
        let route = _routeData["route"][_routeIndex];
        let wayPointIndices = _routeData["wayPointIndices"][_routeIndex];
        let routeLatLng = route.map(coord => L.latLng(coord[1], coord[0]));
        drawRoute(routeLatLng, wayPointIndices, _routeIndex);
        let routeLength = _routeData["routeLength"][_routeIndex];
        if (_routeIndex  <= 0) {
            showPrevRouteButton.classList.add("disabled")
        }else{
            showPrevRouteButton.classList.remove("disabled")
        }
        if (_routeIndex >= _routeData["route"].length-2) {
            showNextRouteButton.classList.add("disabled")
        }else{
            showNextRouteButton.classList.remove("disabled")
        }
        routeTitleElem.innerHTML = `&nbsp;&nbsp;ルート${_routeIndex+1}&nbsp;&nbsp;`;
        routeLengthElem.innerHTML = `${Math.floor((routeLength/1e3) * 100) / 100}&nbsp;km`
        createElevationChart(route);
        let urlPath = newCourseUrl(_routeData, _routeIndex);
        registerCourseLink.href = urlPath;
    }
});
showNextRouteButton.addEventListener('click',function () {
    if (_routeIndex < _routeData["route"].length-2) {//last route data is shortest path, so must eliminate
        clearAllMarker();
        clearAllPolyline();
        _routeIndex++;
        let route = _routeData["route"][_routeIndex];
        let wayPointIndices = _routeData["wayPointIndices"][_routeIndex];
        let routeLatLng = route.map(coord => L.latLng(coord[1], coord[0]));
        drawRoute(routeLatLng, wayPointIndices, _routeIndex);
        let routeLength = _routeData["routeLength"][_routeIndex];
        routeTitleElem.innerHTML = `&nbsp;&nbsp;ルート${_routeIndex+1}&nbsp;&nbsp;`;
        if (_routeIndex  <= 0) {
            showPrevRouteButton.classList.add("disabled")
        }else{
            showPrevRouteButton.classList.remove("disabled")
        }
        if (_routeIndex >= _routeData["route"].length-2) {
            showNextRouteButton.classList.add("disabled")
        }else{
            showNextRouteButton.classList.remove("disabled")
        }
        routeTitleElem.innerHTML = `&nbsp;&nbsp;ルート${_routeIndex+1}&nbsp;&nbsp;`;
        routeLengthElem.innerHTML = `${Math.floor((routeLength/1e3) * 100) / 100}&nbsp;km`
        createElevationChart(route);
        let urlPath = newCourseUrl(_routeData, _routeIndex);
        registerCourseLink.href = urlPath;
    }
});

function clearAllMarker() {
    map.eachLayer(layer => {
        if (layer instanceof L.Polyline) {
            map.removeLayer(layer);
        }
    });
}

function clearAllPolyline() {
    map.eachLayer(layer => {
        if ((layer instanceof L.Marker) && !(layer == startMarker) && !(layer == goalMarker)) {
            map.removeLayer(layer)
        }
    });
}

function fetchRoute(startlatLng, goallatLng) {
    let targetLength = document.getElementById('input-distance').value
    if (!targetLength) {
        targetLength = 0
    }
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
    })
    .then(routeData => {
        let routeIndex = 0;
        _routeData = routeData;
        _routeIndex = routeIndex;
        routeTitleElem.innerHTML = `&nbsp;&nbsp;ルート${_routeIndex+1}&nbsp;&nbsp;`;
        if (_routeIndex  <= 0) {
            showPrevRouteButton.classList.add("disabled")
        }else{
            showPrevRouteButton.classList.remove("disabled")
        }
        if (_routeIndex >= _routeData["route"].length-2) {
            showNextRouteButton.classList.add("disabled")
        }else{
            showNextRouteButton.classList.remove("disabled")
        }
        let route = routeData["route"][routeIndex];
        let wayPointIndices = routeData["wayPointIndices"][routeIndex];
        let routeLatLng = route.map(coord => L.latLng(coord[1], coord[0]));
        drawRoute(routeLatLng, wayPointIndices, routeIndex);
        return routeData
    }).then(
        routeData => {
            let route = routeData["route"][routeIndex];
            let routeLength = routeData["routeLength"][routeIndex];
            document.querySelector('.course-distance').innerHTML = Math.floor((routeLength/1e3) * 100) / 100 + "&nbsp;km"
            createElevationChart(route);
            let urlPath = newCourseUrl(_routeData, _routeIndex);
            registerCourseLink.href = urlPath;
            openResultBar()
        }
    )
    .catch(error => Swal.fire({
            text: error,
            icon: "error",
            backdrop: false
        }))
}

function drawRoute(routeLatLng, wayPointIndices, routeIndex) {
    let routePolyline = L.polyline(routeLatLng, { color: 'red' })
    routePolyline.addTo(map);
    map.fitBounds(routePolyline.getBounds().pad(0.6));

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

function calculateDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // 地球の半径（km）
    var dLat = deg2rad(lat2 - lat1);
    var dLon = deg2rad(lon2 - lon1);
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var distance = R * c; // 距離（km）
    return distance * 1000; // メートルに変換
}

// 度からラジアンに変換
function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

function createElevationChart(route) {
    const existingChart = Chart.getChart("elevation-chart");
    if (existingChart) {
        existingChart.destroy();
    }
    var distanceData = [0];
    distance = 0;
    for (var i = 1; i < route.length; i++) {
        var lat1 = route[i - 1][1];
        var lon1 = route[i - 1][0];
        var lat2 = route[i][1];
        var lon2 = route[i][0];
        var distance = distance + calculateDistance(lat1, lon1, lat2, lon2);
        distanceData.push(distance / 1000);
    }
    let elevationData = route.map(point => point[2]);
    // Canvas要素を取得
    let ctx = document.getElementById('elevation-chart').getContext('2d');
    var elevationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: distanceData,
            datasets: [{
                data: elevationData,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: false,
                pointRadius: 0,
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    ticks: {
                        stepSize: 0.1
                    },
                    title: {
                        display: true,
                        text: '距離 (km)',
                    }
                },
                y: {
                    type: 'linear',
                    position: 'left',
                }
            },
            plugins:{
                legend:{
                    display: false
                }
            }
        }
    });
}

function reverseGeoCoder(latLng) {
    let url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + latLng.lat + '&lon=' + latLng.lng;
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const address = data.display_name;
            return {
                "address": address
            }
        })
        .catch(error => {
            return {
                "address": "選択した場所"
            }
        });
}

function originalGeocoder(query) {
    let url = 'https://nominatim.openstreetmap.org/search?q=' + query + '&format=json&countrycodes=JP';
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }).catch(error => {
            return []
        });
}

function setupAutocomplete(inputElement) {
    const inputElementId = inputElement.getAttribute("id");
    let debounceTimer;

    inputElement.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        document.getElementById('autocomplete-container-' + inputElementId).innerHTML = '';
        debounceTimer = setTimeout(function() {
            containerElement = document.getElementById('autocomplete-container-' + inputElementId)
            const resultList = document.createElement('table');
            if (containerElement) {
                containerElement.appendChild(resultList);
                resultList.classList.add('autocomplete-list');
            } else {
                console.error("Container element not found");
                return;
            }
            const query = inputElement.value;
            originalGeocoder(query)
                .then(data => {
                    // Clear previous results
                    resultList.innerHTML = '';
                    // Display new results
                    data.forEach(result => {
                        const listRow = document.createElement('tr');
                        const listItem = document.createElement('td');
                        var latLng = L.latLng(parseFloat(result.lat), parseFloat(result.lon));
                        listItem.textContent = result.display_name;
                        listItem.addEventListener('click', function() {
                            inputElement.value = result.display_name;
                            resultList.innerHTML = '';
                            map.setView(latLng, 14);
                            if (inputElementId == 'input-start-point') {
                                if (startMarker){
                                    map.removeLayer(startMarker);
                                }
                                startMarker = L.marker(latLng, {icon:startIcon}).addTo(map); 
                                startlatLng = latLng;
                            }
                            else if (inputElementId == 'input-goal-point') {
                                if (goalMarker){
                                    map.removeLayer(goalMarker);
                                }
                                goalMarker = L.marker(latLng, {icon:goalIcon}).addTo(map);
                                goallatLng = latLng;
                            }
                        });
                        listRow.appendChild(listItem);
                        resultList.appendChild(listRow);
                    });
                    if (data.length == 0) {
                        const noListElem = document.createElement('span');
                        noListElem.textContent = "検索結果が見つかりません"
                        resultList.appendChild(noListElem)
                    }
                })
        }, 200); // 500ミリ秒のデバウンス時間
    });

    // Hide results when clicking outside the input and results list
    document.addEventListener('click', function(e) {
        const resultList = document.getElementsByClassName('autocomplete-list')[0];
        if (resultList && !inputElement.contains(e.target) && !resultList.contains(e.target)) {
                resultList.innerHTML = '';
        }
    });
}

function deletePoint(deleteBtn) {
    deleteBtn.addEventListener('click', function() {
        const deleteBtnId = deleteBtn.getAttribute('id');
        const inputElementId = deleteBtnId.replace('delete','input');
        const targetInputElement = document.getElementById(inputElementId);
        targetInputElement.value = '';
        if (inputElementId == 'input-start-point' && startMarker) {
            map.removeLayer(startMarker);
            startMarker = null;
        }else if (inputElementId == 'input-goal-point' && goalMarker) {
            map.removeLayer(goalMarker);
            goalMarker = null;
        }
    })
}

function newCourseUrl(routeData, routeIndex) {
    let route = routeData["route"][routeIndex];
    let routeLatLng = route.map(coord => L.latLng(coord[1], coord[0]));
    let wayPointIndices = routeData["wayPointIndices"][routeIndex];
    let routeLength = Math.floor((routeData["routeLength"][routeIndex]/1e3) * 100) / 100;

    let params = {//ここを修正する。routeIndexとstartLatLng/goalLatLngとユーザーから入力された任意項目のdistanceをparamsに渡し、routeLatLngなどはview側で処理する？
        routeLatLng: JSON.stringify(routeLatLng), // routeをJSON文字列に変換して渡す
        wayPointIndices: JSON.stringify(wayPointIndices), // wayPointIndicesもJSON文字列に変換して渡す
        routeLength: JSON.stringify(routeLength)
    };

    // URLエンコードされたクエリパラメータを作成
    let queryString = Object.keys(params)
    .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&');

    let urlPath = '/courses/new?' + queryString;

    return urlPath
}

function showChoicePopup() {
    return new Promise((resolve, reject) => {
        Swal.fire({
            text: "指定した地点はどちらに登録しますか？",
            showCancelButton: true,
            confirmButtonText: "スタート地点",
            confirmButtonColor: "#3085d6",
            cancelButtonText: "キャンセル",
            cancelButtonColor: "#d33",
            showDenyButton: true,
            denyButtonText: "ゴール地点",
            denyButtonColor: "green",
            icon: "question",
            backdrop: false
        }).then((result) => {
            // ユーザーの選択に基づいて処理を実行
            if (result.isConfirmed) {
                resolve("start"); // "start"を解決
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                resolve("cancel"); // "cancel"を解決
            } else if (result.isDenied) {
                resolve("goal"); // "goal"を解決
            } else {
                reject("No choice made"); // キャンセルや拒否以外の場合はreject
            }
        });
    });
}

function closeSearchBar() {
    const searchBarBtn = document.querySelector('.searchbar-btn');//今回はcloseになっている
    searchBarBtn.classList.remove("close-btn");
    searchBarBtn.classList.add("open-btn");
    searchBarBtn.setAttribute("onclick", "openSearchBar()");
    const searchBarBtnImage = searchBarBtn.getElementsByTagName('i')[0];
    searchBarBtnImage.classList.remove('fa-times');
    searchBarBtnImage.classList.add('fa-bars');
    const searchBarContainer = document.querySelector('.searchbar-content');
    searchBarContainer.classList.remove("expand")
    searchBarContainer.classList.add("shrink")
    const routeContainer = document.querySelector('.route-container');
    routeContainer.classList.remove("expand")
    routeContainer.classList.add("shrink")
}

function openSearchBar() {
    const searchBarBtn = document.querySelector('.searchbar-btn');//今回はopenになっている
    searchBarBtn.classList.remove("open-btn")
    searchBarBtn.classList.add("close-btn")
    searchBarBtn.setAttribute("onclick", "closeSearchBar()");
    const searchBarBtnImage = searchBarBtn.getElementsByTagName('i')[0];
    searchBarBtnImage.classList.remove('fa-bars');
    searchBarBtnImage.classList.add('fa-times');
    const searchBarContainer = document.querySelector('.searchbar-content');
    searchBarContainer.classList.remove("shrink")
    searchBarContainer.classList.add("expand")
    const routeContainer = document.querySelector('.route-container');
    routeContainer.classList.remove("shrink")
    routeContainer.classList.add("expand")
}

function closeResultBar() {
    const searchBarBtn = document.querySelector('.searchbar-btn');//今回はcloseになっている
    searchBarBtn.classList.remove("close-btn");
    searchBarBtn.classList.add("open-btn");
    searchBarBtn.setAttribute("onclick", "openSearchBar()");
    const searchBarBtnImage = searchBarBtn.getElementsByTagName('i')[0];
    searchBarBtnImage.classList.remove('fa-times');
    searchBarBtnImage.classList.add('fa-bars');
    const searchBarContainer = document.querySelector('.searchbar-content');
    searchBarContainer.classList.remove("expand")
    searchBarContainer.classList.add("shrink")
    const routeContainer = document.querySelector('.route-container');
    routeContainer.classList.remove("expand")
    routeContainer.classList.add("shrink")
}

function openResultBar() {
    const resultBarContainer = document.querySelector('.resultbar-container');
    resultBarContainer.classList.remove("none");
    resultBarContainer.classList.remove("hidden");
    resultBarContainer.classList.add("show");
    const resultBarBtn = document.querySelector('.resultbar-handle');
    resultBarBtn.setAttribute("onclick", "hideResultBar()")
    const resultBarBtnImage = resultBarBtn.getElementsByTagName('i')[0];
    resultBarBtnImage.classList.remove('fa-caret-left');
    resultBarBtnImage.classList.add('fa-caret-right');
}

function hideResultBar() {
    const resultBarContainer = document.querySelector('.resultbar-container');
    resultBarContainer.classList.remove("none");
    resultBarContainer.classList.remove("show");
    resultBarContainer.classList.add("hidden");
    const resultBarBtn = document.querySelector('.resultbar-handle');
    resultBarBtn.setAttribute("onclick", "openResultBar()")
    const resultBarBtnImage = resultBarBtn.getElementsByTagName('i')[0];
    resultBarBtnImage.classList.remove('fa-caret-right');
    resultBarBtnImage.classList.add('fa-caret-left');
}