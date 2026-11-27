import json
import heapq
from pathlib import Path


BASE_DIR = Path(__file__).parent
ADJACENCY_FILE = BASE_DIR / "output" / "adjacency_list.json"


def load_graph(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    graph = {}
    for node, neighbors in data.items():
        graph.setdefault(int(node), [])
        for neighbor, weight in neighbors:
            graph[int(node)].append((int(neighbor), weight))
            graph.setdefault(int(neighbor), [])
    return graph

def dijkstra(graph, start, end):
    """Return (path, distance_in_meters). If there is no path: ([], inf)."""
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous = {}
    queue = [(0, start)]

    while queue:
        dist, current = heapq.heappop(queue)
        if current == end:
            break
        if dist > distances[current]:
                continue
        for neighbor, weight in graph[current]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(queue, (new_dist, neighbor))

    if distances[end] == float("inf"):
        return [], float("inf")

    path = [end]
    while path[-1] != start:
        path.append(previous[path[-1]])
    return path[::-1], distances[end]

if __name__ == "__main__":
        graph = load_graph(ADJACENCY_FILE)
        nodes = list(graph.keys())
        path, distance = dijkstra(graph, nodes[0], nodes[-1])
        print("Nodes:", len(graph))
        print("Path:", path)
        print("Distance (m):", round(distance, 2))
