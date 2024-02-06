import osmnx as ox
import networkx as nx
import numpy as np
import pandas as pd

def get_route_length(graph, route):
  """
  経路の長さを計算

  Args:
    graph: 道路ネットワークグラフ
    route: 経路のノードリスト

  Returns:
    経路の長さ (m)
  """

  route_length = 0
  for i in range(len(route) - 1):
    u, v = route[i], route[i + 1]
    edge_length = nx.shortest_path_length(graph, u, v, weight="length")
    route_length += edge_length
  return route_length

def score_neighbor_node(graph, gdf, start_node, prev_node, current_node, neighbor_node, end_node):
  x_start, y_start = gdf.loc[gdf.index==start_node,["x","y"]].iloc[0]
  x_current, y_current = gdf.loc[gdf.index==current_node,["x","y"]].iloc[0]
  x_neighbor, y_neighbor = gdf.loc[gdf.index==neighbor_node,["x","y"]].iloc[0]
  x_end, y_end = gdf.loc[gdf.index==end_node,["x","y"]].iloc[0]
  x_prev, y_prev = gdf.loc[gdf.index==prev_node,["x","y"]].iloc[0]
  vec_current_to_neighbor = np.array([x_neighbor - x_current, y_neighbor - y_current])
  vec_prev_to_current = np.array([x_current - x_prev, y_current - y_prev])
  norm_vec_current_to_neighbor = np.linalg.norm(vec_current_to_neighbor)
  norm_vec_prev_to_current = np.linalg.norm(vec_prev_to_current)
  prod = np.dot(vec_current_to_neighbor, vec_prev_to_current)
  if (norm_vec_prev_to_current <= 10e-10) or (norm_vec_current_to_neighbor <= 10e-10):
    cosine = 0.5
  else:
    cosine = prod / (norm_vec_current_to_neighbor*norm_vec_prev_to_current)
  cosine_score = cosine
  shortest_path_length_between_neighbor_and_end = nx.shortest_path_length(graph, neighbor_node, end_node, weight="length")
  shortest_path_length_between_current_and_neighbor = nx.shortest_path_length(graph, current_node, neighbor_node, weight="length")
  score = (shortest_path_length_between_neighbor_and_end + shortest_path_length_between_current_and_neighbor) * cosine_score
  return score

def extend_route(graph, gdf, route, target_distance_min):

  if len(route) == 1:
    route = [route[0] , route[0]]
  extended_route = route[:]
  prev_node = route[0]
  start_node = route[0]
  current_node = route[0]
  end_node = route[-1]
  remove_nodes = []
  longest_extended_route_length = 0
  longest_extended_route = extended_route
  while True:
    route_length = get_route_length(graph, extended_route)
    if route_length > longest_extended_route_length:
      longest_extended_route_length = route_length
      longest_extended_route = extended_route
    current_node_index = extended_route.index(current_node)
    print(route_length)
    if (route_length < target_distance_min) and (current_node_index <= len(extended_route)-2):
      neighbor_nodes = graph.neighbors(current_node)
      neighbor_nodes = [neighbor_node for neighbor_node in neighbor_nodes if neighbor_node not in remove_nodes]
      sorted_neighbor_nodes = sorted(neighbor_nodes, key=lambda neighbor_node: score_neighbor_node(graph, gdf, start_node, prev_node, current_node, neighbor_node, end_node),reverse=True)
      for neighbor_node in sorted_neighbor_nodes:
        if neighbor_node not in extended_route:
          extended_route = extended_route[:current_node_index+1] + nx.shortest_path(graph, neighbor_node, end_node, weight="length")
          prev_node = current_node
          current_node = neighbor_node
          break
      updated_route_length = get_route_length(graph, extended_route)
      if updated_route_length <= route_length:
          print("Remove: ", current_node)
          remove_nodes.append(current_node)
          extended_route = extended_route[:current_node_index] + extended_route[current_node_index+1:]
          current_node = extended_route[current_node_index-1]
          prev_node = extended_route[current_node_index-2]
    else:
      break
  return longest_extended_route

def get_nodes_coordinates(gdf, route):
    df_route = pd.DataFrame(route, columns=["osmid"])
    gdf = gdf.reset_index()
    df_merged = pd.merge(df_route,gdf,how="left",on="osmid")[["y","x"]]
    return df_merged.values.tolist()

def plan_route(G, start_point, end_point, target_distance_min):
    start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
    end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

    # A*アルゴリズムによる最短経路探索
    route = nx.shortest_path(G, start_node, end_node, weight="length")
    route_length = get_route_length(G, route)

    if route_length < target_distance_min:
        print(f"route_length: {route_length}, target_distance_min: {target_distance_min}")
        gdf = ox.graph_to_gdfs(G, nodes=True, edges=False)
        route = extend_route(G, gdf, route, target_distance_min)
        print(f"longest route length: {get_route_length(G,route)}")
        print(f"intersecrtions in longest route: {len(route)-1}")
    print("探索終了")
    route = get_nodes_coordinates(gdf,route)

    return route, route_length