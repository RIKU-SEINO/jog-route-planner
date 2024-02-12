from flask import Blueprint, render_template, request, jsonify, send_from_directory
import requests

route_map = Blueprint(
    'route_map',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/map',
)

def execute_search(y_start, x_start, y_end, x_end, target_length):
    url = f"https://trailrouter.com/ors/experimentalroutes?coordinates={x_start},{y_start}%7C{x_end},{y_end}&skip_segments=&green_preference=0.8&avoid_unsafe_streets=false&avoid_unlit_streets=false&hills_preference=0&avoid_repetition=true&target_distance={target_length}&roundtrip=false"
    res = requests.get(url)
    data = res.json()
    route = data["routes"][0]["geometry"]["coordinates"]
    route_length = data["routes"][0]["distance"]
    way_points = data["routes"][0]["waypoints"]
    return route, route_length, way_points


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
            route, route_length, way_points = execute_search(y_start, x_start, y_goal, x_goal, target_length)
            return jsonify({'route': route, 
                            'routeLngth': route_length,
                            'wayPoints': way_points})
        except Exception as e:
            return jsonify({'error': str(e)})
    return render_template('map/index.html')

@route_map.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('route_map/templates/map', filename)