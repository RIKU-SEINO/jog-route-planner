from flask import Blueprint, render_template, request, jsonify
import requests

route_map = Blueprint(
    'route_map',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/map',
)

def execute_search(y_start, x_start, y_end, x_end, target_length):
    if (y_start == y_end) and (x_start == x_end):
        roundtrip_option = "true"
    else:
        roundtrip_option = "false"
    url = f"https://trailrouter.com/ors/experimentalroutes?coordinates={x_start},{y_start}%7C{x_end},{y_end}&skip_segments=&green_preference=&avoid_unsafe_streets=false&avoid_unlit_streets=false&hills_preference=0&avoid_repetition=true&target_distance={target_length}&roundtrip={roundtrip_option}"
    res = requests.get(url)
    data = res.json()
    return data


@route_map.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        try:
            data = request.get_json()
            y_start = float(data["startlat"])
            x_start = float(data["startlng"])
            y_goal = float(data["goallat"])
            x_goal = float(data["goallng"])
            target_length = int(float(data["targetLength"])*1e3) # convert to km
            data = execute_search(y_start, x_start, y_goal, x_goal, target_length)
            route_data_list = data["routes"]
            route_list, route_length_list, way_point_indices_list = [], [], []
            for i in range(len(route_data_list)):
                route = route_data_list[i]["geometry"]["coordinates"]
                route_list.append(route)
                route_length = route_data_list[i]["distance"]
                route_length_list.append(route_length)
                way_point_indices = route_data_list[i]["waypointIndices"]
                way_point_indices_list.append(way_point_indices)
            return jsonify({'route': route_list, 
                            'routeLength': route_length_list,
                            'wayPointIndices': way_point_indices_list})
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('create_route.html')