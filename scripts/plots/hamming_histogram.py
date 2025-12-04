import csv
import matplotlib.pyplot as plt

csv_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/biological_jpeg_tiff_mapping_test.csv"
output_png = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/plots/hamming_histogram_logscale.png"

hamming_values = []

# --- Load Hamming distance values from CSV ---
with open(csv_path, "r") as f:
    reader = csv.reader(f)

    # Skip header row
    next(reader, None)

    for row in reader:
        if len(row) < 4:
            continue

        hamming = int(row[-4])  # fourth-last column (Hamming distance)
        hamming_values.append(hamming)

# --- Plot histogram with log-scale frequency ---
plt.figure(figsize=(10, 5))
plt.hist(hamming_values, bins=30, edgecolor="black", log=True)
plt.title("Histogram of Hamming Distance — Log Frequency")
plt.xlabel("Hamming Distance")
plt.ylabel("Frequency (log scale)")
plt.tight_layout()

# Save as PNG
plt.savefig(output_png, dpi=300)
plt.close()

print(f"Log-scale Hamming histogram saved as: {output_png}")
