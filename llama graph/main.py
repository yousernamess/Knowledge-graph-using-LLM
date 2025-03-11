import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


# Load JSON file
with open('output.json', 'r') as file:
    data = json.load(file)


nodes = set()
edges = []

for relation in data:
    node_1 = relation['node_1']
    node_2 = relation['node_2']
    edge = relation['edge']
    
    nodes.add(node_1)
    nodes.add(node_2)
    edges.append((node_1, node_2, edge))



# Initialize a graph
G = nx.Graph()

# Add nodes and edges
for node in nodes:
    G.add_node(node)

for node_1, node_2, edge in edges:
    G.add_edge(node_1, node_2, label=edge)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.write_graphml(G, "knowledge_graph.graphml")

plt.show()
