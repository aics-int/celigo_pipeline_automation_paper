import os
import pandas as pd
import fire
from shutil import copy2

def merge_csvs_and_copy_png(input_path, output_path, target_file_name="ColonyDATA.csv"):
    """
    Concatenates all CSV files with a specific name in the subfolders of the given folder
    into a single CSV file, and copies PNG files to an "Outlines" folder in the output path.

    Parameters:
        input_path (str): The input folder containing subfolders with CSV files.
        output_path (str): The output path to store concatenated CSV file and "Outlines" folder.
        target_file_name (str): The name of the target CSV files to concatenate (default is "ColonyDATA.csv").
    """

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    outlines_folder = os.path.join(output_path, "Outlines")
    # Create the "Outlines" subfolder if it doesn't exist
    if not os.path.exists(outlines_folder):
        os.makedirs(outlines_folder)

    output_csv_file = os.path.join(output_path, target_file_name)
    all_dataframes = []  # Store all dataframes to be concatenated

    # Loop through the subfolders
    for subdir, _, files in os.walk(input_path):
        for file_name in files:
            file_path = os.path.join(subdir, file_name)
            destination_path = os.path.join(outlines_folder, file_name)

            # If the file is the target CSV, read it into a DataFrame
            if file_name == target_file_name:
                df = pd.read_csv(file_path)
                all_dataframes.append(df)

            # If the file is a PNG, copy it to the "Outlines" subfolder
            elif file_name.endswith('.png') and file_path != destination_path:
                copy2(file_path, destination_path)

    # Concatenate all dataframes and write to the output CSV
    concatenated_df = pd.concat(all_dataframes, ignore_index=True)
    concatenated_df.to_csv(output_csv_file, index=False)

    print(f"CSV files named {target_file_name} have been concatenated into {output_csv_file}")
    print(f"All PNG files have been copied to {outlines_folder}")

if __name__ == '__main__':
    fire.Fire(merge_csvs_and_copy_png)
