"""
# Creates a network graph of professors based on their co-authorship connections.
# Created by Thien An Tran on 4/12/2024
# Last modified on 5/20/2024
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re
import time
import random


def search_google_scholar(first_name, last_name, school):
    """ Search Google Scholar for the given professor's profile and return the profile URL. 
    (only needed if the source of the professor is not provided in the dataset)
    """
    query = f"{first_name} {last_name} {school}"
    base_url = "https://scholar.google.com/scholar?hl=en&q="
    search_url = base_url + "+".join(query.split())
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        # 'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        # 'User-agent': 'Super Bot Power Level Over 9000'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 429:
        print("Rate limit hit during query, try again later")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    profile_link = None
    for link in soup.find_all('h4', class_='gs_rt2'):
        profile_link = "https://scholar.google.com" + link.a['href']
        break  # Assumes the first result is the correct profile

    return profile_link


def get_coauthors(profile_url):
    """ Retrieve the co-authors of a professor given their Google Scholar profile URL."""
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
    """ Recursively adds co-authors to the graph from a starting professor's Google Scholar profile if they are also in the dataset."""
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


def save_graph(G, filename="network_graph.pdf"):
    """ Save the network graph of professors to a PDF file. """
    # Extracting node names as a list
    node_names = list(G.nodes())

    # Extract ethnicity information from the DataFrame for processed professors
    ethnicity_series = df.set_index('Full Name')['Actual'].to_dict()

    for node in node_names:
        if node in ethnicity_series:
            G.nodes[node]['Actual'] = ethnicity_series[node]
        else:
            G.nodes[node]['Actual'] = 'Unknown'

    # Mapping ethnicity to color
    ethnicity_color_map = {
        'White': 'lightblue',
        'Asian': 'lightgreen',
        'Black': 'lightcoral',
        'Other': 'lightyellow',
        'Unknown': 'lightgrey'  # Default color for unknown ethnicity
    }

    # Assign color to nodes based on ethnicity
    node_colors = [ethnicity_color_map.get(G.nodes[node].get('Actual', 'Unknown'), 'lightgrey') for node in G.nodes()]

    print("Saving graph now...")
    plt.figure(figsize=(100, 100))
    nx.draw(G, with_labels=True, node_color=node_colors, edge_color='#909090', node_size=1000, font_size=9, alpha=0.6, linewidths=0.5)

    # Create a list of legend handles:
    legend_handles = [mpatches.Patch(color=color, label=ethnicity) for ethnicity, color in ethnicity_color_map.items()]
    # Add the legend to the plot
    plt.legend(handles=legend_handles, title='Ethnicity')

    plt.title('Co-Authorship Graph Among UC Professors')
    plt.savefig(filename, format='pdf')
    # plt.show()
    plt.close()


if __name__ == '__main__':

    # Prepare dataset and graph
    df = pd.read_csv('UC_first200_actual_cleaned.csv')
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']  # Create a Full Name column to simplify searches

    G = nx.Graph()  # Undirected graph to represent co-authorship connections
    visited = set() # Keep track of visited professors to avoid cycles

    # Process each professor in the dataset
    try:
        for index, row in df.iterrows():
            full_name = row['Full Name']
            if full_name not in visited:
                try:
                    #   profile_url = search_google_scholar(row['First Name'], row['Last Name'], row['School'])
                    profile_url = row['Source']
                    if profile_url:
                        add_coauthors_to_graph(full_name, profile_url, G, df, visited)

                        print(f"Finished processing {full_name}")

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching data for {full_name}: {e}")
                    continue  # Skip to the next professor

    except Exception as e:
        print(e)

    finally:
        save_graph(G, "UC_first200_network_graph.pdf")
        print("Graph has been saved.")