from flask import Flask, Blueprint, render_template, request
import osmnx as ox
import json
from shapely.geometry import box
from threading import Thread
from utils.utils import CustomThread
import threading

route_map = Blueprint(
    'route_map',
    __name__,
    static_folder='static',
    template_folder='templates',
    url_prefix='/map',
)

ox.config(use_cache=False, log_console=True)

def fetch_graph_data(bounds):
    west, south, east, north = list(map(float, bounds.split(",")))
    bbox = box(west, south, east, north)
    custom_filter = '["highway"~"|footway|path|steps"]["footway"!="crossing"]["highway"!="pedestrian"]["access"!="private"]'
    print("地図読込み開始")
    G = ox.graph_from_polygon(bbox, network_type='walk', custom_filter=custom_filter)
    print("地図読込み終了")
    return G

@route_map.route("/",methods=["POST","GET"])
def home():
    if request.method == "POST":
        bounds = request.json["bounds"]
        thread = CustomThread(target=fetch_graph_data, args=(bounds,))
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


    return render_template('map/index.html')

def process_graph(G):
    return {"nodes": list(G.nodes), "edges": list(G.edges)}