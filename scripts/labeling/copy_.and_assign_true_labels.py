import os
import stat
import shutil
import pandas as pd

# Path to your CSV file
csv_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/n_tiff_to_all_jpeg_mapping/1000_tiff.csv"

# Folder where the renamed TIFFs will be copied
output_folder = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/labeled_tif/1000_tif"
os.makedirs(output_folder, exist_ok=True)



# Read the CSV
df = pd.read_csv(csv_path)

# Process each row
for _, row in df.iterrows():

    # Skip rows that were not a match
    if not row["used_ssim"]:
        continue

    tiff_path = row['TIFF_path']
    jpeg_file = row['JPEG_file']
    
    # Take first three characters of JPEG file name
    prefix = jpeg_file[:3]
    
    # Get TIFF file extension
    tiff_filename = row['TIFF_file']
    
    # New TIFF file name
    new_tiff_name = f"{prefix}{tiff_filename}"
    
    # Destination path
    dest_path = os.path.join(output_folder, new_tiff_name)
    
    # Copy TIFF to new folder with new name
    shutil.copy2(tiff_path, dest_path)
    
    print(f"Copied {tiff_path} to {dest_path}")
