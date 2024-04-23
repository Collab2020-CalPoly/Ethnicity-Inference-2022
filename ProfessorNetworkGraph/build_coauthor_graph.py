"""
# Creates a network graph of professors based on their co-authorship connections.
# Created by Thien An Tran on 4/12/2024
# Last modified on 4/18/2024
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

def search_google_scholar(first_name, last_name):
    """ Search Google Scholar for the given professor's profile and return the profile URL. """
    query = f"{first_name} {last_name}"
    base_url = "https://scholar.google.com/scholar?hl=en&q="
    search_url = base_url + "+".join(query.split())
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        # 'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        # 'User-agent': 'Super Bot Power Level Over 9000'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 429:
        print("Rate limit hit during coauthors retrieval, try again later")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    profile_link = None
    for link in soup.find_all('h4', class_='gs_rt2'):
        profile_link = "https://scholar.google.com" + link.a['href']
        break  # Assumes the first result is the correct profile

    return profile_link


def get_coauthors(profile_url):
    if profile_url is None:
        return []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(profile_url, headers=headers)
    if response.status_code == 429:
        print("Rate limit hit during coauthors retrieval, try again later")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    coauthors_section = soup.find('div', id='gsc_rsb_co')
    coauthors = []

    if coauthors_section:
        for coauthor in coauthors_section.find_all('div', class_='gsc_rsb_aa'):
            name_link = coauthor.find('a')
            if name_link:
                coauthor_name = name_link.text.strip()
                coauthor_profile = "https://scholar.google.com" + name_link['href']
                coauthors.append((coauthor_name, coauthor_profile))

    return coauthors


def add_coauthors_to_graph(full_name, profile_url, G, df, visited):
    """ Recursively adds co-authors to the graph from a starting professor's Google Scholar profile. """
    if full_name in visited:
        return
    visited.add(full_name)  # Mark this node as visited
    G.add_node(full_name) # Add the initial professor as a node (is it needed? In case there's a prof with no connections)
    coauthors = get_coauthors(profile_url)
    if not coauthors:  # If no coauthors, this is a terminal node
        return

    for coauthor_name, coauthor_url in coauthors:
        if df['Full Name'].str.contains(re.escape(coauthor_name), regex=True, na=True).any():
            if coauthor_name not in visited:  # Prevent cycles
                G.add_edge(full_name, coauthor_name)  # Add an edge between the original professor and the co-author
                print(coauthor_name)
                add_coauthors_to_graph(coauthor_name, coauthor_url, G, df, visited)  # Recursive call using the direct URL


# Prepare your dataset and graph
df = pd.read_csv('./cleaningdata/modelResults.csv')
df['Full Name'] = df['First Name'] + ' ' + df['Last Name']  # Create a Full Name column to simplify searches
G = nx.Graph()
visited = set()

# Mapping ethnicity to color
ethnicity_color_map = {
    'White': 'lightblue',
    'Asian': 'lightgreen',
    'Black': 'lightcoral',
    'Other': 'lightyellow',
    'Unknown': 'lightgrey'  # Default color for unknown ethnicity
}

### ALL PROFESSOR IN DATASET
# # Start the graph construction from each professor's initially known profile URL
# for index, row in df.iterrows():
#     full_name = row['Full Name']
#     if full_name not in visited:
#         profile_url = search_google_scholar(row['First Name'], row['Last Name'])  # Initial search to get the profile URL
#         print(profile_url)
#         add_coauthors_to_graph(full_name, profile_url, G, df, visited)
#     print(f"Finished processing {full_name}")

## ONE SPECIFIC PROFESSOR FROM DATASET
# # Select the specific professor you want to work with
# professor_index = 0  # Change this index to select a different professor
# selected_professor = df.iloc[professor_index]
# full_name = selected_professor['Full Name']
# profile_url = search_google_scholar(selected_professor['First Name'], selected_professor['Last Name'])
# add_coauthors_to_graph(full_name, "https://scholar.google.com/citations?user=vtwH6GkAAAAJ&hl=en", G, df, visited)


### N PROFESSOR FROM DATASET
n_professors = 15  # Change this to the desired number of professors

# Start the graph construction from each professor's initially known profile URL
processed_professors = 0
for index, row in df.iterrows():
    if processed_professors >= n_professors:
        break  # Exit loop if the desired number of professors is reached
    
    full_name = row['Full Name']
    if full_name not in visited:
        profile_url = search_google_scholar(row['First Name'], row['Last Name'])  # Initial search to get the profile URL
        if profile_url:  # Check if a profile URL is retrieved successfully
            add_coauthors_to_graph(full_name, profile_url, G, df, visited)
            processed_professors += 1
            print(f"Finished processing {full_name} ({processed_professors}/{n_professors})")


# Extracting node names as a list
node_names = list(G.nodes())

# Extract ethnicity information from the DataFrame for processed professors
ethnicity_series = df.set_index('Full Name').loc[node_names, 'Prediction']

# Assign ethnicity information to nodes in the graph
for node in node_names:
    if node in ethnicity_series.index:
        G.nodes[node]['Prediction'] = ethnicity_series[node]
    else:
        # Handle case where ethnicity information is missing
        G.nodes[node]['Prediction'] = 'Unknown'

# Assign color to nodes based on ethnicity
node_colors = [ethnicity_color_map.get(ethnicity, 'lightgrey') for ethnicity in ethnicity_series]


# Visualize the graph
print("visualizing graph now...")
plt.figure(figsize=(12, 12))
# nx.draw(G, with_labels=True, node_color='lightblue', edge_color='#909090', node_size=500, font_size=9, alpha=0.6, linewidths=0.5)
nx.draw(G, with_labels=True, node_color=node_colors, edge_color='#909090', node_size=500, font_size=9, alpha=0.6, linewidths=0.5)
plt.title('Co-Authorship Graph Among UC Professors')
# plt.savefig('co_authorship_graph.png')
plt.show()