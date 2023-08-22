import pandas as pd
import os
import fire
import math

"""
Example usage:
python well_qc_score.py --csv_path="path/to/your/input.csv"

Args:
    csv_path (str): Path to the input CSV file
"""

def calculate_values(group):
        
    group["Confluency"] = (
        group["AreaOccupied_AreaOccupied_Colony"].mean()
        / group["AreaOccupied_AreaOccupied_WellObjects"].mean()
    )

    group["Estimated_Cell_Count"] = 0.212940459 * math.exp(
        0.000000116541332 * group["AreaOccupied_AreaOccupied_Colony"].mean()
    )
    return group

def filter_and_add_calculated_columns(csv_path):
    # Columns to filter
    columns_to_filter = [
        'Metadata_Plate',
        'Metadata_Well',
        'Metadata_DateString',
        'AreaOccupied_AreaOccupied_Colony',
        'AreaOccupied_AreaOccupied_WellObjects',
    ]

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Keep only the columns needed and initialize new columns
    df = df[columns_to_filter]
    df['Confluency'] = 0
    df['Estimated_Cell_Count'] = 0

    # Group by plate, well, and date string, then apply the calculate_values function
    df = df.groupby(['Metadata_Plate', 'Metadata_Well', 'Metadata_DateString'], group_keys=False).apply(calculate_values) # Updated groupby here

    # Reorder columns
    df = df[
        [
            'Metadata_Plate',
            'Metadata_Well',
            'Metadata_DateString',
            'AreaOccupied_AreaOccupied_Colony',
            'AreaOccupied_AreaOccupied_WellObjects',
            'Confluency',
            'Estimated_Cell_Count',
        ]
    ]

    # Generate output filename with "_WellConfluency" suffix
    file_path, file_extension = os.path.splitext(csv_path)
    output_file_path = file_path + "_WellConfluency" + file_extension

    # Save the filtered dataframe to the new CSV file
    df.to_csv(output_file_path, index=False)
    print(f"WellConfluency CSV file with calculated values and comments saved to {output_file_path}")

if __name__ == '__main__':
    fire.Fire(filter_and_add_calculated_columns)