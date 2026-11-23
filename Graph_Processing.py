import csv

nodes = {}
graph = {}

# Read nodes
with open("output/nodes.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        node_id = int(row["node_id"])

        nodes[node_id] = {
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"])
        }

        graph[node_id] = []

print(f"Loaded {len(nodes)} nodes.")


with open("output/edges.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        source = int(row["source"])
        destination = int(row["destination"])
        weight = float(row["weight_meters"])

        if source not in graph or destination not in graph:
            raise ValueError("Edge references an unknown node")

        if weight <= 0:
            raise ValueError("Road distance must be positive")

        graph[source].append((destination, weight))

print("Adjacency list created successfully!")

print("\nFirst 5 nodes and their connections:")

for node_id in list(graph)[:5]:
    print(f"{node_id}: {graph[node_id]}")



def reachable_nodes(graph, start):
    visited = set()
    stack = [start]

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        for neighbor, weight in graph[current]:
            if neighbor not in visited:
                stack.append(neighbor)

    return visited


start_node = next(iter(graph))
reachable = reachable_nodes(graph, start_node)

print(f"\nStarting node: {start_node}")
print(f"Reachable nodes: {len(reachable)}")
print(f"Total nodes: {len(graph)}")
print(f"Reachable percentage: {len(reachable) / len(graph) * 100:.2f}%")

unreachable = set(graph.keys()) - reachable

print("\nUnreachable nodes:")

for node in unreachable:
    print(
        f"Node: {node}",
        f"Coordinates: {nodes[node]}"
    )



print("\nAnalyzing unreachable nodes:")

for node in unreachable:
    outgoing = len(graph[node])

    incoming = sum(
        1
        for source in graph
        for neighbor, weight in graph[source]
        if neighbor == node
    )

    print(f"\nNode: {node}")
    print(f"Incoming edges: {incoming}")
    print(f"Outgoing edges: {outgoing}")


    def dfs_component(graph, start, visited):
        stack = [start]
        component = []

        while stack:
            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)
            component.append(node)

            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

        return component


    # Kosaraju's algorithm
    def strongly_connected_components(graph):
        visited = set()
        finish_order = []

        # First DFS pass: finishing order
        for start in graph:
            if start in visited:
                continue

            stack = [(start, False)]

            while stack:
                node, processed = stack.pop()

                if processed:
                    finish_order.append(node)
                    continue

                if node in visited:
                    continue

                visited.add(node)
                stack.append((node, True))

                for neighbor, weight in graph[node]:
                    if neighbor not in visited:
                        stack.append((neighbor, False))

        # Reverse every directed edge
        reversed_graph = {node: [] for node in graph}

        for source, neighbors in graph.items():
            for destination, weight in neighbors:
                reversed_graph[destination].append((source, weight))

        # Second DFS pass
        visited.clear()
        components = []

        for node in reversed(finish_order):
            if node not in visited:
                component = dfs_component(
                    reversed_graph, node, visited
                )
                components.append(component)

        return components


    components = strongly_connected_components(graph)
    largest = max(components, key=len)

    print(f"\nStrongly connected components: {len(components)}")
    print(f"Largest component: {len(largest)} nodes")
    print(f"Percentage: {len(largest) / len(graph) * 100:.2f}%")

    import networkx as nx

    # Create a directed graph for verification
    G_check = nx.DiGraph()

    G_check.add_nodes_from(graph.keys())

    for source, neighbors in graph.items():
        for destination, weight in neighbors:
            G_check.add_edge(source, destination)

    # Calculate strongly connected components
    components_check = list(
        nx.strongly_connected_components(G_check)
    )

    largest_check = max(components_check, key=len)

    print("\n--- Connectivity verification ---")
    print(f"Components: {len(components_check)}")
    print(f"Largest component: {len(largest_check)} nodes")
    print(f"Percentage: {len(largest_check) / len(graph) * 100:.2f}%")


import json
from pathlib import Path

output = Path("output")
output.mkdir(exist_ok=True)

# Export the complete weighted adjacency list
with open(output / "adjacency_list.json", "w") as file:
    json.dump(graph, file, indent=2)

# Export the largest strongly connected component
largest_nodes = set(largest_check)

connected_graph = {
    node: [
        (neighbor, weight)
        for neighbor, weight in graph[node]
        if neighbor in largest_nodes
    ]
    for node in largest_nodes
}

with open(output / "connected_graph.json", "w") as file:
    json.dump(connected_graph, file, indent=2)

print("\nGraph exports completed!")