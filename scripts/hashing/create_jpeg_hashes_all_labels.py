# SPDX-FileCopyrightText: 2025 Jacopo Zuppa Riccardo Simonetti Sandeep Chavuladi Roberta Lamberti
#
# SPDX-License-Identifier: MIT

import os
import imagehash
from PIL import Image, ImageOps
import pandas as pd
from tqdm import tqdm

# Top-level folder containing many subfolders with JPEGs
jpeg_root = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/public_dataset/Complete_dataset"

output_csv = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/jpeg_hashes_all_labels.csv"

def standardize_image(pil_img):
    if pil_img.mode != 'L':
        pil_img = pil_img.convert('L')
    pil_img = ImageOps.equalize(pil_img)
    pil_img = ImageOps.autocontrast(pil_img)
    return pil_img

def compute_hash(image_path, hash_size=32):
    try:
        pil_img = Image.open(image_path)
        pil_img_std = standardize_image(pil_img)
        phash = imagehash.phash(pil_img_std, hash_size=hash_size)
        return str(phash)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

# --- Recursively find ALL JPEG files ---
jpeg_files = []
for root, dirs, files in os.walk(jpeg_root):
    for f in files:
        if f.lower().endswith((".jpg", ".jpeg")):
            jpeg_files.append(os.path.join(root, f))

print(f"Found {len(jpeg_files)} JPEG images across all subfolders.")

# --- Compute hashes ---
jpeg_hash_list = []
for f in tqdm(jpeg_files):
    h = compute_hash(f)
    if h is not None:
        jpeg_hash_list.append({
            "file": os.path.basename(f),
            "path": f,
            "phash": h
        })

# --- Save to CSV ---

pd.DataFrame(jpeg_hash_list).to_csv(output_csv, index=False)

print(f"Saved {len(jpeg_hash_list)} JPEG hashes to {output_csv}")

