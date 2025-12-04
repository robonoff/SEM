import csv
import os

csv_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/biological_jpeg_tiff_mapping_test.csv"

mismatches = []
checked = 0

with open(csv_path, "r") as f:
    reader = csv.reader(f)

    # Skip header
    next(reader, None)

    for row in reader:
        if len(row) < 4:
            continue

        rating = row[-1].strip().lower()

        # Only check "excellent"
        if rating == "excellent":
            checked += 1

            jpeg_name = os.path.basename(row[0])       # column 1
            tiff_name = os.path.basename(row[2])       # column 3

            jpeg_base = os.path.splitext(jpeg_name)[0]
            tiff_base = os.path.splitext(tiff_name)[0]

            if jpeg_base != tiff_base:
                mismatches.append((jpeg_name, tiff_name))

# --- Summary ---
print(f"Checked {checked} rows with SSIM rating == 'excellent'.")

if mismatches:
    print("\n❌ Mismatched file name pairs:")
    for j, t in mismatches:
        print(f"  JPEG: {j}  |  TIFF: {t}")
else:
    print("\n✔ All 'excellent' rows have matching JPEG/TIFF base filenames.")
