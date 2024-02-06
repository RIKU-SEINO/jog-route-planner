from math import radians, sin, cos, sqrt, atan2
import osmnx as ox

def haversine_distance(start_point, end_point):
    # 地球の半径（単位: km）
    R = 6371.0
    # 緯度経度をラジアンに変換
    lat1, lon1 = radians(start_point[0]), radians(start_point[1])
    lat2, lon2 = radians(end_point[0]), radians(end_point[1])
    # 差の計算
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # 距離を計算
    distance = R * c * 1000
    return distance

def fetch_graph(lat_lon):
    start_point =  (float(lat_lon[0]["lat"]), float(lat_lon[0]["lng"]))
    end_point = (float(lat_lon[1]["lat"]), float(lat_lon[1]["lng"]))
    center_point = (start_point[0]+end_point[0])/2, (start_point[1]+end_point[1])/2
    dist = haversine_distance(start_point=start_point, end_point=end_point)
    custom_filter = '["highway"~"|footway|path|steps"]["footway"!="crossing"]["highway"!="pedestrian"]["access"!="private"]'
    print("地図読込み開始")
    G = ox.graph_from_point(center_point=center_point, dist=dist, network_type='walk', custom_filter=custom_filter)
    print("地図読込み終了")
    return G, start_point, end_point