import csv
import matplotlib.pyplot as plt

csv_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/biological_jpeg_tiff_mapping_test.csv"
output_png = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/plots/ssim_histogram_logscale.png"

ssim_values = []

# --- Load SSIM values from CSV ---
with open(csv_path, "r") as f:
    reader = csv.reader(f)

    # Skip header row
    next(reader, None)

    for row in reader:
        if len(row) < 3:
            continue

        ssim = float(row[-3])  # third-last column
        ssim_values.append(ssim)

# --- Plot histogram with log-scale frequency ---
plt.figure(figsize=(10, 5))
plt.hist(ssim_values, bins=30, edgecolor="black", log=True)
plt.title("Histogram of Structural Similarity (SSIM) — Log Frequency")
plt.xlabel("SSIM Value")
plt.ylabel("Frequency (log scale)")
plt.tight_layout()

# Save as PNG
plt.savefig(output_png, dpi=300)
plt.close()

print(f"Log-scale histogram saved as: {output_png}")

