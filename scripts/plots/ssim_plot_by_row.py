import csv
import matplotlib.pyplot as plt

csv_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/biological_jpeg_tiff_mapping_test.csv"
output_png = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/plots/ssim_plot.png"

ssim_values = []

with open(csv_path, "r") as f:
    reader = csv.reader(f)

    # Skip header
    next(reader, None)

    for row in reader:
        if len(row) < 3:
            continue

        ssim = float(row[-3])  # third-last column
        ssim_values.append(ssim)

# --- Plot and save ---
plt.figure(figsize=(12, 5))
plt.plot(ssim_values, marker="o")
plt.title("Structural Similarity (SSIM) Values")
plt.xlabel("Row index")
plt.ylabel("SSIM")
plt.grid(True)
plt.tight_layout()

plt.savefig(output_png, dpi=300)   # save as PNG
plt.close()  # close figure

print(f"Plot saved as: {output_png}")

