import pandas as pd
import os
import fire

"""
Example usage:
python well_qc_score.py --csv_path="path/to/your/input.csv" --low_confluency_threshold=0.25 --high_confluency_threshold=0.85

Args:
    csv_path (str): Path to the input CSV file
    low_confluency_threshold (float): Low confluency threshold for calculation. Default is 0.25.
    high_confluency_threshold (float): High confluency threshold for calculation. Default is 0.85.
    The high and low confluency thresholds are optional arguments and will use defaults if not passed in.  We have determined that 25000px^2 is the minimum area of a colony we want to image.  This value will need to be adjusted based on your imaging criteria.
"""

def calculate_values(group, low_confluency_threshold, high_confluency_threshold):
    # Calculate confluency
    group['confluency'] = group['AreaShape_Area'].sum() / 1510564

    # Initialize comment column
    group['Comment'] = ""

    # Check confluency threshold
    if not low_confluency_threshold <= group['confluency'].mean() <= high_confluency_threshold:
        group['Comment'] += "Confluency out of acceptable range; "

    # Calculate the number of colonies greater and less than 25000
    group['ColoniesGreater_than_25000'] = (group['AreaShape_Area'] > 25000).sum()
    group['ColoniesLess_than_25000'] = (group['AreaShape_Area'] < 25000).sum()

    # Check other conditions and add to comment if they fail
    if group['Children_BallCraterClassifiedObjects_Count'].sum() > 5:
        group['Comment'] += "BallCrater objects count greater than 5; "
    if group['ColoniesGreater_than_25000'].mean() < 1:
        group['Comment'] += "# of Colonies greater than 25000 less than 1; "
    if group['Children_EdgeClassifiedObjects_Count'].sum() > 10:
        group['Comment'] += "Edge objects count greater than 10; "

    # Determine final QC Score
    if group['Comment'].any():
        group['Well_QC_Score'] = "Fail"
    else:
        group['Well_QC_Score'] = "Pass"

    return group

def filter_and_add_calculated_columns(csv_path, low_confluency_threshold=0.25, high_confluency_threshold=0.85):
    # Columns to filter
    columns_to_filter = [
        'Metadata_Plate',
        'Metadata_Well',
        'Metadata_DateString',
        'ObjectNumber',
        'AreaShape_Area',
        'Children_BallCraterClassifiedObjects_Count',
        'Children_EdgeClassifiedObjects_Count'
    ]

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Keep only the columns needed
    df = df[columns_to_filter]

    # Add calculated columns with empty values
    df['ColoniesGreater_than_25000'] = 0
    df['ColoniesLess_than_25000'] = 0
    df['confluency'] = 0
    df['Well_QC_Score'] = ""
    df['Comment'] = ""

    # Group by plate, well, and date string, then apply the calculate_values function
    df = df.groupby(['Metadata_Plate', 'Metadata_Well', 'Metadata_DateString'], group_keys=False).apply(calculate_values, low_confluency_threshold, high_confluency_threshold) # Updated groupby here

    # Reorder columns
    df = df[['Metadata_Plate', 'Metadata_Well', 'Metadata_DateString', 'ObjectNumber', 'AreaShape_Area', 'Children_BallCraterClassifiedObjects_Count', 'Children_EdgeClassifiedObjects_Count', 'ColoniesGreater_than_25000', 'ColoniesLess_than_25000', 'confluency', 'Well_QC_Score', 'Comment']]

    # Generate output filename with "_WellQCScore" suffix
    file_path, file_extension = os.path.splitext(csv_path)
    output_file_path = file_path + "_WellQCScore" + file_extension

    # Save the filtered dataframe to the new CSV file
    df.to_csv(output_file_path, index=False)
    print(f"WellQCScore CSV file with calculated values and comments saved to {output_file_path}")

if __name__ == '__main__':
    fire.Fire(filter_and_add_calculated_columns)
