import pandas as pd

def filter_players(file1, file2, output_file):
    # Read the clarafai file
    clarafai_df = pd.read_csv(file1)
    
    # Read the namsor file
    namsor_df = pd.read_csv(file2)
    
    # Get the list of namsor names
    target_names = namsor_df[['First Name', 'Last Name']]
    
    # Filter the cleaned MLB players
    valid_players_df = clarafai_df[clarafai_df[['First Name', 'Last Name']].apply(tuple, axis=1).isin(target_names.apply(tuple, axis=1))]
    
    # Write the valid players to the output file
    valid_players_df.to_csv(output_file, index=False)

# Define the file paths
clarafai_csv = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/mlb_cropped_output_old_cols.csv'
namsor_csv = 'C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/Namsor/namsorOutputGT.csv'
output_file = 'overlap.csv'

# Call the function to filter the players
filter_players(clarafai_csv, namsor_csv, output_file)
