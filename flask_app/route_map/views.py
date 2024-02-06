from flask import Blueprint, render_template, request, jsonify
import osmnx as ox
import networkx as nx
from utils.custom_thread import CustomThread
import threading
from math import radians, sin, cos, sqrt, atan2
import numpy as np
from flask_app.route_map.route_lib.fetch_graph import fetch_graph
from flask_app.route_map.route_lib.plan_route import plan_route

route_map = Blueprint(
    'route_map',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/map',
)

def execute_search(lat_lon, target_distance_min):
    G, start_point, end_point = fetch_graph(lat_lon=lat_lon)
    route, route_length = plan_route(G=G,start_point=start_point, end_point=end_point, target_distance_min=target_distance_min)
    return route, route_length

@route_map.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        lat_lon = (request.json["startlatLng"], request.json["endlatLng"])
        target_distance_min = 5000
        route, route_length = execute_search(lat_lon=lat_lon, target_distance_min=target_distance_min)

        '''
        thread = CustomThread(target=execute_search, args=(lat_lon,target_distance_min))
        current_threads = threading.enumerate()
        print(current_threads)
        print("上がカレンとスレッド！！！！")
        for current_thread in current_threads:
            try:
                current_thread.raise_exception()
                print(f"{str(current_thread)}を中止しました。")
            except:
                print(f"{str(current_thread)}は中止できません。")
        thread.start()
        print(f"{str(thread)}が追加されました")
        print("中止後")
        print(threading.enumerate())
        print("\n\n\n")
        thread.join()
        '''
        print(route)
        return jsonify({'route': route, 'route_length': route_length})
    return render_template('map/index.html')

def process_graph(G):
    return {"nodes": list(G.nodes), "edges": list(G.edges)}