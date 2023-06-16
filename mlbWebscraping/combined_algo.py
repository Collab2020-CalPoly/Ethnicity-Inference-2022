import pandas as pd

def process_input_file(input_file, output_file, ground_truth):
    # Read the input file as a pandas DataFrame
    input_df = pd.read_csv(input_file)
    
    # Compare Clarafai-Confidence and Namsor-probabilityCalibrated columns
    input_df["Winner"] = ""
    input_df["NC-prediction"] = ""
    
    for index, row in input_df.iterrows():
        clarafai_confidence = row["Clarafai-Confidence"]
        namsor_probability = row["Namsor-probabilityCalibrated"]
        clarafai_ground_truth = row["Clarafai-Ground_Truth"]
        namsor_ground_truth = row["Namsor-Ground_Truth"]
        
        if clarafai_confidence > namsor_probability:
            input_df.at[index, "Winner"] = "Clarafai"
            input_df.at[index, "NC-prediction"] = clarafai_ground_truth
        elif clarafai_confidence < namsor_probability:
            input_df.at[index, "Winner"] = "Namsor"
            input_df.at[index, "NC-prediction"] = namsor_ground_truth
        else:
            input_df.at[index, "Winner"] = "Tie"
            input_df.at[index, "NC-prediction"] = clarafai_ground_truth
    
    # Create the output DataFrame with selected columns
    output_df = input_df[["First Name", "Last Name", "Clarafai-Prediction", "Clarafai-Confidence", "Namsor-raceEthnicity", "Namsor-probabilityCalibrated", "Winner", "NC-prediction"]]
    
    # Populate Ground_Truth from previous csv
    ground_truth_df = pd.read_csv(ground_truth)
    # Merge the ground truth data based on First Name and Last Name columns
    merged_df = pd.merge(output_df, ground_truth_df, on=["First Name", "Last Name"], how="left")
    # Populate the Ground_Truth column with overlapping names
    merged_df["Ground_Truth"] = merged_df["Ground_Truth"].fillna("")
    merged_df = merged_df.drop(["White", "Black", "Asian", "Other", "Prediction", "Confidence"], axis=1)
    
    # Write the output DataFrame to the output file
    merged_df.to_csv(output_file, index=False)

# Define the input and output file paths
input_file = "combined_merged_output.csv"
output_file = "output.csv"
ground_truth = "clarafai_old_cols.csv"

# Call the function to process the input file and write the output to a new CSV file
process_input_file(input_file, output_file, ground_truth)
