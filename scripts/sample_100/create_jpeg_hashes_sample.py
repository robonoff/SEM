import os
import imagehash
from PIL import Image, ImageOps
import pandas as pd
import numpy as np
from tqdm import tqdm
import random

# Paths
jpeg_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/public_dataset/Complete_dataset/Tips"
tiff_path = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/backup_folder"


def standardize_image(pil_img):
    # convert to grayscale (if not already in grayscale)
    if pil_img.mode != 'L':
        pil_img = pil_img.convert('L')
    # better contrast
    pil_img = ImageOps.equalize(pil_img)
    # normalization
    pil_img = ImageOps.autocontrast(pil_img)
    return pil_img

def compute_hash(image_path, hash_size=32):
    try:
        pil_img = Image.open(image_path)
        pil_img_std = standardize_image(pil_img)
        phash = imagehash.phash(pil_img_std, hash_size=hash_size)
        return str(phash)  # store as string
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

# --- Process JPEGs ---
jpeg_files = [os.path.join(jpeg_path, f) for f in os.listdir(jpeg_path) if f.lower().endswith((".jpg", ".jpeg"))]

N = 100  # number of random files you want
jpeg_subset = random.sample(jpeg_files, min(N, len(jpeg_files)))

jpeg_hash_list = []
for f in tqdm(jpeg_subset):
    h = compute_hash(f)
    if h is not None:
        jpeg_hash_list.append({
            "file": os.path.basename(f),
            "path": f,
            "phash": h
        })

jpeg_df = pd.DataFrame(jpeg_hash_list)
jpeg_df.to_csv("/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/tips_jpeg_tiff_mapping.csv", index=False)
print(f"Saved {len(jpeg_df)} JPEG hashes to Label_jpeg_hashes.csv")

