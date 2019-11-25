import csv
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = []
with open('sample.txt') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        node1 = int(row[0].strip())
        node2 = int(row[1].strip())
        weight = float(row[2].strip())
        color = str(row[3].strip())
        edge = (node1, node2, {'weight': weight, 'color': color})
        edges.append(edge)
        
G.add_edges_from(edges)
t = G.edges[1,3]
print(t)
#print(G.edges.data('weight'))
#print(l)
#plt.subplot(121)
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()
