"""
# Creates a network graph of professors based on their co-authorship connections.
# Created by Thien An Tran on 4/12/2024
# Last modified on 6/1/2024
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
import matplotlib.backends.backend_pdf
import scipy as sp


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

    # Excluding the base case: algorithm doesn't prematurely stop exploring co-authors, allowing more connections (edges) to be made.
    # When the base case is excluded, the function doesn't halt upon encountering a visited node. This continuation allows the function to explore all reachable nodes and their connections.
    # It does lead to redundant processing though (e.g., revisiting nodes), but it ensures that all possible connections are made.
    # if full_name in visited:
    #     return  # Stop processing if this professor has been visited already

    # Retrieve co-authors regardless of whether the current professor has been visited or not
    coauthors = get_coauthors(profile_url)

    for coauthor_name, coauthor_url in coauthors:
        if df['Full Name'].str.contains(re.escape(coauthor_name), regex=True, na=True).any():
            # Check if the edge already exists to prevent adding it twice
            if not G.has_edge(full_name, coauthor_name):
                G.add_edge(full_name, coauthor_name)  # Add an edge only if it does not already exist
                print(f"Edge added between {full_name} and {coauthor_name}")
            if coauthor_name not in visited:  # Check if co-author has been visited
                visited.add(coauthor_name)  # Mark co-author as visited
                add_coauthors_to_graph(coauthor_name, coauthor_url, G, df, visited)  # Recursive call for the co-author

    # Mark the current professor as visited after all possible edges are added
    visited.add(full_name)


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


def filter_dataset_based_on_graph(G, original_df):
    """ Filter the original DataFrame to include only professors who are part of a connected component in the graph. """
    # Get all nodes in the connected components
    connected_nodes = set()
    
    # for node in G.nodes:
    #     if node not in nx.connected_components(G):
    #         G.remove_node(node)

    for component in nx.connected_components(G):
        connected_nodes.update(component)

    # Filter the DataFrame to include only these nodes
    filtered_df = original_df[original_df['Full Name'].isin(connected_nodes)]
    
    return filtered_df


if __name__ == '__main__':

    # Prepare dataset and graph
    df = pd.read_csv('UCB_UCLA_first1000_results_actual.csv')
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

        # # Filter dataset based on connected components in the graph
        # filtered_df = filter_dataset_based_on_graph(G, df)
        # filtered_df.to_csv('Filtered_UCB_UCLA_1500_test.csv', index=False)  # Save the filtered dataset
        # print("Filtered dataset has been saved.")

        save_graph(G, "UCB_UCLA_first1000_results_actual_TEST.pdf")
        print("Graph has been saved.")
        print(f"Graph has {len(G.nodes)} nodes and {len(G.edges)} edges.")