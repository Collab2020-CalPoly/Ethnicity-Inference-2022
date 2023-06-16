import pandas as pd

def process_csv_file(csv_file):
    data = pd.read_csv(csv_file)

    # Replace values in the "Ground_Truth" column
    data.loc[data['Ground_Truth'].isin(['Indian', 'Latino_Hispanic']), 'Ground_Truth'] = 'Other'

    # Write the updated data back to the CSV file
    data.to_csv(csv_file, index=False)


process_csv_file("C:/MAVACResearchMugizi/Winter2023/mlbWebscraping/Namsor/namsorOutputGT.csv")
