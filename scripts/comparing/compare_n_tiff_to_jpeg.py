import os
import random
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim
import imagehash

# -----------------------------
# USER INPUT
# -----------------------------
JPEG_CSV = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/jpeg_hashes_all_labels.csv"
TIFF_CSV = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/tiff_hashes.csv"
N_TIFF = 1000             # number of random TIFFs to consider
OUTPUT_CSV = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/n_tiff_to_all_jpeg_mapping/1000_tiff.csv"

TOP_K = 2                 # number of JPEGs with lowest Hamming to consider
HAMMING_THRESHOLD = 150    # fallback threshold for Hamming
SSIM_THRESHOLD = 0.70      # min SSIM to consider good match

# -----------------------------
# HELPERS
# -----------------------------
def load_image_array(path):
    try:
        img = Image.open(path)
        if img.mode != 'L':
            img = img.convert('L')
        img = ImageOps.equalize(img)
        img = ImageOps.autocontrast(img)
        return np.array(img)
    except Exception:
        return None

def compute_ssim(a1, a2):
    if a1 is None or a2 is None:
        return 0.0
    if a1.shape != a2.shape:
        from skimage.transform import resize
        a2 = resize(a2, a1.shape, anti_aliasing=True, preserve_range=True).astype(a1.dtype)
    return ssim(a1, a2, data_range=a1.max() - a1.min())

# -----------------------------
# LOAD DATA
# -----------------------------
jpeg_df = pd.read_csv(JPEG_CSV)
jpeg_df["phash_obj"] = jpeg_df["phash"].apply(lambda x: imagehash.hex_to_hash(x))
print(f"Loaded {len(jpeg_df)} JPEG entries.")

tiff_df = pd.read_csv(TIFF_CSV)
tiff_df["phash_obj"] = tiff_df["phash"].apply(lambda x: imagehash.hex_to_hash(x))
print(f"Loaded {len(tiff_df)} TIFF entries.\n")

# -----------------------------
# SELECT RANDOM TIFF SUBSET
# -----------------------------
N_TIFF = min(N_TIFF, len(tiff_df))
tiff_subset = tiff_df.sample(N_TIFF, random_state=42).reset_index(drop=True)
print(f"Selected {len(tiff_subset)} random TIFF images for matching.\n")

# -----------------------------
# MATCHING
# -----------------------------
matches = []

for _, trow in tqdm(tiff_subset.iterrows(), total=len(tiff_subset), desc="Processing TIFFs"):
    t_path = trow["path"]
    t_hash = trow["phash_obj"]

    # 1️⃣ Compute Hamming distances to all JPEGs
    jpeg_df["hamming_dist"] = jpeg_df["phash_obj"].apply(lambda jh: jh - t_hash)

    # 2️⃣ Take TOP_K lowest Hamming distances
    top_candidates = jpeg_df.nsmallest(TOP_K, "hamming_dist")

    t_array = None
    best_ssim = -1
    best_jpeg = None
    best_hamming = None
    used_ssim = False

    for _, jrow in top_candidates.iterrows():
        j_path = jrow["path"]
        hamming_dist = jrow["hamming_dist"]

        ssim_score = None
        local_used_ssim = False

        # Compute SSIM if Hamming is low enough
        if hamming_dist < HAMMING_THRESHOLD:
            if t_array is None:
                t_array = load_image_array(t_path)
            j_array = load_image_array(j_path)
            ssim_score = compute_ssim(j_array, t_array)
            local_used_ssim = True

        # Decide best match
        if local_used_ssim:
            if ssim_score > best_ssim:
                best_ssim = ssim_score
                best_jpeg = j_path
                best_hamming = hamming_dist
                used_ssim = True
        else:
            if best_jpeg is None:
                best_jpeg = j_path
                best_hamming = hamming_dist

    # Save the best match for this TIFF
    matches.append({
        "TIFF_file": os.path.basename(t_path),
        "TIFF_path": t_path,
        "JPEG_file": os.path.basename(best_jpeg) if best_jpeg else None,
        "JPEG_path": best_jpeg,
        "hamming_distance": best_hamming,
        "ssim_score": best_ssim if used_ssim else None,
        "used_ssim": used_ssim
    })

# -----------------------------
# SAVE RESULTS
# -----------------------------
match_df = pd.DataFrame(matches)
match_df.to_csv(OUTPUT_CSV, index=False)

print(f"\nSaved {len(match_df)} TIFF → best JPEG matches to {OUTPUT_CSV}")
print(match_df.head())
