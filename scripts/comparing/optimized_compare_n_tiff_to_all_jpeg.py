# SPDX-FileCopyrightText: 2025 Jacopo Zuppa Riccardo Simonetti Sandeep Chavuladi Roberta Lamberti
#
# SPDX-License-Identifier: MIT

import os
import pandas as pd
import numpy as np
from PIL import Image, ImageOps
from tqdm import tqdm
from skimage.transform import resize
import imagehash
import torch
import torch.nn.functional as F

# -----------------------------
# USER INPUT
# -----------------------------
JPEG_CSV = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/jpeg_hashes_all_labels.csv"
TIFF_CSV = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/tiff_hashes.csv"
N_TIFF = 9905
OUTPUT_CSV = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/n_tiff_to_all_jpeg_mapping/all_tiff.csv"
TOP_K = 2
HAMMING_THRESHOLD = 150
SSIM_THRESHOLD = 0.70
BATCH_SIZE = 100  # adjust batch size for memory efficiency
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# HELPERS
# -----------------------------
def load_image_array(path):
    """Load image, convert to grayscale, equalize and autocontrast"""
    try:
        img = Image.open(path)
        if img.mode != 'L':
            img = img.convert('L')
        img = ImageOps.equalize(img)
        img = ImageOps.autocontrast(img)
        return np.array(img, dtype=np.float32) / 255.0  # normalize
    except Exception:
        return None

def compute_ssim_torch(a1, a2, eps=1e-6):
    """Compute SSIM between two 2D numpy arrays on GPU"""
    if a1.shape != a2.shape:
        a2 = resize(a2, a1.shape, anti_aliasing=True, preserve_range=True).astype(np.float32)
    a1_t = torch.from_numpy(a1).unsqueeze(0).unsqueeze(0).to(DEVICE)
    a2_t = torch.from_numpy(a2).unsqueeze(0).unsqueeze(0).to(DEVICE)
    kernel_size = 11
    sigma = 1.5
    coords = torch.arange(kernel_size).float() - kernel_size // 2
    g = torch.exp(-(coords ** 2) / (2 * sigma ** 2))
    g /= g.sum()
    g2d = g[:, None] * g[None, :]
    g2d = g2d.unsqueeze(0).unsqueeze(0).to(DEVICE)
    mu1 = F.conv2d(a1_t, g2d, padding=kernel_size//2)
    mu2 = F.conv2d(a2_t, g2d, padding=kernel_size//2)
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = F.conv2d(a1_t**2, g2d, padding=kernel_size//2) - mu1_sq
    sigma2_sq = F.conv2d(a2_t**2, g2d, padding=kernel_size//2) - mu2_sq
    sigma12 = F.conv2d(a1_t*a2_t, g2d, padding=kernel_size//2) - mu1_mu2
    C1 = 0.01 ** 2
    C2 = 0.03 ** 2
    ssim_map = ((2*mu1_mu2 + C1)*(2*sigma12 + C2)) / ((mu1_sq + mu2_sq + C1)*(sigma1_sq + sigma2_sq + C2) + eps)
    return ssim_map.mean().item()

def phash_to_bits(phash_obj):
    """Convert imagehash object to 64-bit array safely"""
    val = int(str(phash_obj), 16)
    return np.array(list(np.binary_repr(val, width=64)), dtype=np.uint8)

# -----------------------------
# LOAD DATA
# -----------------------------
jpeg_df = pd.read_csv(JPEG_CSV)
jpeg_df["phash_obj"] = jpeg_df["phash"].apply(imagehash.hex_to_hash)
print(f"Loaded {len(jpeg_df)} JPEG entries.")

tiff_df = pd.read_csv(TIFF_CSV)
tiff_df["phash_obj"] = tiff_df["phash"].apply(imagehash.hex_to_hash)
print(f"Loaded {len(tiff_df)} TIFF entries.\n")

# -----------------------------
# SELECT RANDOM TIFF SUBSET
# -----------------------------
N_TIFF = min(N_TIFF, len(tiff_df))
tiff_subset = tiff_df.sample(N_TIFF, random_state=42).reset_index(drop=True)
print(f"Selected {len(tiff_subset)} random TIFF images for matching.\n")

# -----------------------------
# PREPARE JPEG HASH BITS
# -----------------------------
jpeg_bits = np.stack([phash_to_bits(p) for p in jpeg_df["phash_obj"]])

# -----------------------------
# BATCHED HAMMING DISTANCES
# -----------------------------
matches = []

print("Processing TIFFs in batches...")
for start_idx in tqdm(range(0, len(tiff_subset), BATCH_SIZE), desc="Batches"):
    end_idx = min(start_idx + BATCH_SIZE, len(tiff_subset))
    t_batch = tiff_subset.iloc[start_idx:end_idx]
    t_bits = np.stack([phash_to_bits(p) for p in t_batch["phash_obj"]])

    # Compute Hamming distances: shape (batch_size, n_jpeg)
    # XOR and count bits
    xor_result = np.bitwise_xor(t_bits[:, None, :], jpeg_bits[None, :, :])
    hamming_dists = xor_result.sum(axis=2)

    for i, trow in enumerate(t_batch.itertuples(index=False)):
        top_indices = np.argsort(hamming_dists[i])[:TOP_K]
        best_jpeg_path = None
        best_hamming = None
        best_ssim = -1
        used_ssim = False
        t_array = None

        for idx in top_indices:
            jrow = jpeg_df.iloc[idx]
            hd = hamming_dists[i, idx]
            if hd < HAMMING_THRESHOLD:
                if t_array is None:
                    t_array = load_image_array(trow.path)
                j_array = load_image_array(jrow.path)
                if t_array is not None and j_array is not None:
                    ssim_score = compute_ssim_torch(j_array, t_array)
                    if ssim_score > best_ssim:
                        best_ssim = ssim_score
                        best_jpeg_path = jrow.path
                        best_hamming = hd
                        used_ssim = True
            else:
                if best_jpeg_path is None:
                    best_jpeg_path = jrow.path
                    best_hamming = hd

        matches.append({
            "TIFF_file": os.path.basename(trow.path),
            "TIFF_path": trow.path,
            "JPEG_file": os.path.basename(best_jpeg_path) if best_jpeg_path else None,
            "JPEG_path": best_jpeg_path,
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
