
from pathlib import Path
import osmnx as ox
import pandas as pd


METROCENTRO = (12.12801, -86.26486)
DISTANCE = 1500

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

ox.settings.use_cache = True


print("Downloading Metrocentro road network...")

G = ox.graph.graph_from_point(
    METROCENTRO,
    dist=DISTANCE,
    network_type="drive",
    simplify=True
)

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")

# 3. Extract nodes and edges
nodes, edges = ox.convert.graph_to_gdfs(G)

# 4. Prepare nodes table
nodes_df = pd.DataFrame({
    "node_id": nodes.index,
    "latitude": nodes["y"].values,
    "longitude": nodes["x"].values
})

# 5. Prepare directed edges table
edges_df = edges.reset_index()[
    ["u", "v", "key", "length"]
].rename(columns={
    "u": "source",
    "v": "destination",
    "length": "weight_meters"
})

# 6. Export CSV files
nodes_df.to_csv(OUTPUT / "nodes.csv", index=False)
edges_df.to_csv(OUTPUT / "edges.csv", index=False)

# 7. Save the complete graph
ox.io.save_graphml(G, filepath=OUTPUT / "metrocentro.graphml")

# 8. Save a visualization
fig, ax = ox.plot.plot_graph(
    G,
    node_size=8,
    edge_linewidth=0.7,
    show=False,
    close=True
)
fig.savefig(OUTPUT / "road_network.png", dpi=200)

print("Export completed successfully!")
