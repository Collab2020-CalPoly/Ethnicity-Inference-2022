import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def count_matches(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Create a mapping for the categories
    category_mapping = {
        'White': 'White',
        'Black': 'Black',
        'Asian': 'Asian',
        'Other': 'Other',
        'Latino_Hispanic': 'Other'
    }

    # Map the categories in the "NC-prediction" column to the corresponding categories in the mapping
    df['NC-prediction'] = df['NC-prediction'].map(category_mapping)

    # Count the matches between "NC-prediction" and "Ground_Truth" columns
    matches = (df['NC-prediction'] == df['Ground_Truth']).sum()
    
    # Calculate the total number of rows
    total_rows = len(df)

    # Calculate the percentage of matches
    percentage_matches = (matches / total_rows) * 100

    # Calculate the ratio of matches
    ratio_matches = matches / total_rows

    # Print the number of matches, percentage, and ratio
    print(f"Number of matches: {matches} : {total_rows}")
    print(f"Percentage of matches: {percentage_matches:.2f}%")
    print(f"Ratio of matches: {ratio_matches:.4f}")
    
    # Create a confusion matrix
    confusion_matrix = pd.crosstab(df['Ground_Truth'], df['NC-prediction'])
    
    # Print the pairs of matches per group
    pairs = df.groupby(['NC-prediction', 'Ground_Truth']).size().reset_index(name='count')
    print(pairs)

    
    # Visualize the confusion matrix using seaborn
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_matrix, annot=True, cmap="YlGnBu", fmt="d")
    plt.xlabel('NC-prediction')
    plt.ylabel('Ground_Truth')
    plt.title('Confusion Matrix')
    plt.show()

    # Return the number of matches
    return matches

count = count_matches("C:\MAVACResearchMugizi\Winter2023\mlbWebscraping\combined_output.csv")
