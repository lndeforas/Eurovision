import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("year")
parser.add_argument("type")
args = parser.parse_args()
year = int(args.year)
type = int(args.type)

df = pd.read_csv("votes.csv")

types = ["total_points", "tele_points", "jury_points"]

def heatmap(year,t):
    df_sup = df[df["year"]>=year]
    points = df_sup.groupby(["to_country_id", "from_country_id"])[types[t]].sum().unstack(fill_value=0)
    plt.figure(figsize=(14, 9))
    sns.heatmap(points, cmap="coolwarm")
    plt.title(f"Heatmap of votes exchanged between countries between {year} and 2023")
    plt.savefig(f"images/heatmap_sup_{year}_{types[t]}")
    return points

def graphe(year, t):
    total_points = heatmap(year,t)
    
    if t!=0:
        coef = (2024-year)*11
    else:
        coef = (2024-year)*16
    
    total_points_bin = total_points.map(lambda x: np.where(x<coef, 0, 1))

    G = nx.from_pandas_adjacency(total_points_bin, create_using=nx.DiGraph())

    isolates = list(nx.isolates(G))
    G.remove_nodes_from(isolates)

    pos = nx.spring_layout(G, weight='weight', k=0.5, iterations=50) 

    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(G, pos, node_color='lightpink', node_size=300)
    nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
    for (u, v, d) in G.edges(data=True):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=(total_points.loc[u, v]/25-coef/20))

    plt.title(f"Network of votes sent between {year} and 2023")
    plt.axis('off')
    plt.savefig(f"images/graphe_sup_{year}_{types[t]}")
    
graphe(year, type)