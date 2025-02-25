import pandas as pd
import networkx as nx
from pyvis.network import Network

# Load IIT and NIT professor data
iit_df = pd.read_csv("iitb_professor_citation_data.csv")
nit_df = pd.read_csv("nitb_professor_citation_data.csv")

# Create NetworkX Graph
G = nx.Graph()

# Add IIT professors (Red)
iit_profs = set(iit_df.iloc[:, 0])
for prof in iit_profs:
    G.add_node(prof, color="red", title=prof)  # Tooltip text

# Add NIT professors (Blue)
nit_profs = set(nit_df.iloc[:, 0])
for prof in nit_profs:
    G.add_node(prof, color="blue", title=prof)

# Extract and add co-authors
iit_coauthors = set()
for coauthors in iit_df.iloc[:, -1]:  # Last column contains co-authors
    if isinstance(coauthors, str):
        coauthors = eval(coauthors) if coauthors.startswith("[") else []
        iit_coauthors.update(coauthors)

nit_coauthors = set()
for coauthors in nit_df.iloc[:, -1]:
    if isinstance(coauthors, str):
        coauthors = eval(coauthors) if coauthors.startswith("[") else []
        nit_coauthors.update(coauthors)

# Common co-authors (Green)
common_coauthors = iit_coauthors.intersection(nit_coauthors)
for author in common_coauthors:
    G.add_node(author, color="green", title="Common Co-author")

# Other co-authors (Gray)
other_coauthors = (iit_coauthors.union(nit_coauthors)) - common_coauthors - iit_profs - nit_profs
for author in other_coauthors:
    G.add_node(author, color="gray", title="Other Co-author")

# Add edges between professors and co-authors
for _, row in iit_df.iterrows():
    prof = row.iloc[0]
    if isinstance(row.iloc[-1], str):
        coauthors = eval(row.iloc[-1]) if row.iloc[-1].startswith("[") else []
        for coauthor in coauthors:
            G.add_edge(prof, coauthor)

for _, row in nit_df.iterrows():
    prof = row.iloc[0]
    if isinstance(row.iloc[-1], str):
        coauthors = eval(row.iloc[-1]) if row.iloc[-1].startswith("[") else []
        for coauthor in coauthors:
            G.add_edge(prof, coauthor)

# Convert NetworkX graph to Pyvis Network
net = Network(notebook=True, height="800px", width="100%", bgcolor="#222222", font_color="white")
net.from_nx(G)

# Set node physics for better visualization
net.repulsion(node_distance=150, central_gravity=0.2, spring_length=200, damping=0.09)

# Save and display the graph
net.show("coauthorship_network.html")
