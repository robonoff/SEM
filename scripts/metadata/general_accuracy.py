import csv
import os
from collections import defaultdict

csv_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/biological_jpeg_tiff_mapping_test.csv"

# Data structure to store results per category
stats = defaultdict(lambda: {"correct": 0, "wrong": 0, "pairs": []})

with open(csv_path, "r") as f:
    reader = csv.reader(f)
    next(reader, None)  # skip header

    for row in reader:
        if len(row) < 4:
            continue

        category = row[-1].strip().lower()  # e.g., excellent, good, no_match

        jpeg_name = os.path.basename(row[0])
        tiff_name = os.path.basename(row[2])

        jpeg_base = os.path.splitext(jpeg_name)[0]
        tiff_base = os.path.splitext(tiff_name)[0]

        # Determine correctness
        if category == "no_match":
            is_correct = jpeg_base != tiff_base
        else:
            is_correct = jpeg_base == tiff_base

        if is_correct:
            stats[category]["correct"] += 1
        else:
            stats[category]["wrong"] += 1
            stats[category]["pairs"].append((jpeg_name, tiff_name))

# --- Print per-category statistics ---
print("\n===== CATEGORY-WISE ACCURACY REPORT =====\n")

total_correct = 0
total_wrong = 0

# Ensure no category is skipped, including 'no_match'
for category in stats:
    info = stats[category]
    correct = info["correct"]
    wrong = info["wrong"]
    total = correct + wrong

    acc = (correct / total) * 100 if total > 0 else 0

    print(f"Category: {category}")
    print(f"  Total rows: {total}")
    print(f"  Correct: {correct}")
    print(f"  Wrong: {wrong}")
    print(f"  Accuracy: {acc:.2f}%")

    if wrong > 0:
        print("  Mismatched pairs:")
        for j, t in info["pairs"]:
            print(f"    JPEG: {j} | TIFF: {t}")

    print()

    total_correct += correct
    total_wrong += wrong

# --- Global accuracy ---
global_total = total_correct + total_wrong
global_acc = (total_correct / global_total) * 100 if global_total > 0 else 0

print("===== OVERALL ACCURACY =====")
print(f"Total rows: {global_total}")
print(f"Total correct: {total_correct}")
print(f"Total wrong: {total_wrong}")
print(f"Overall accuracy: {global_acc:.2f}%")
