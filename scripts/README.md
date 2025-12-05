# Scripts Documentation

This folder contains Python scripts for processing and analyzing the SEM dataset. Scripts are organized by function into subdirectories.

## Overview

The processing pipeline converts TIFF microscopy images to JPEG format, generates perceptual hashes for similarity matching, and maps converted images back to their originals.

## Directory Structure

```
scripts/
├── hashing/                    # Generate perceptual hashes
│   ├── create_jpeg_hashes_all_labels.py
│   └── create_jpeg_hashes_single_label.py
├── comparing/                  # Match JPEGs to original TIFFs
│   ├── compare_n_tiff_to_jpeg.py
│   └── optimized_compare_n_tiff_to_all_jpeg.py
├── labeling/                   # Assign category labels to files
│   └── copy_.and_assign_true_labels.py
└── csv/                        # Generated data files
    └── n_tiff_to_all_jpeg_mapping/
```

## Scripts

### Root Level

### `hashing/`

Generate perceptual hashes (pHash) for images to enable similarity matching.

#### `create_jpeg_hashes_all_labels.py`

Generates pHash for all JPEG images in the complete dataset.

**What it does:**
- Recursively finds all JPEG files in specified directory
- Applies standardization: grayscale conversion, histogram equalization, auto-contrast
- Computes 32×32 perceptual hash for each image
- Outputs CSV with columns: `file`, `path`, `phash`

**Output:** `csv/jpeg_hashes_all_labels.csv`

#### `create_jpeg_hashes_single_label.py`

Generates pHash for images belonging to a single category.

**What it does:**
- Same processing as `create_jpeg_hashes_all_labels.py`
- Processes only one category folder at a time
- Useful for memory-constrained environments or incremental processing

**Output:** `csv/single_label_jpeg_hashes/{category}_complete_jpeg_hashes.csv`

### `comparing/`

Match converted JPEG images to their original TIFF files using perceptual hashing and similarity metrics.

#### `compare_n_tiff_to_jpeg.py`

Compares N randomly selected TIFFs with the entire JPEG dataset.

**What it does:**
- Loads perceptual hashes for both JPEG and TIFF images
- For each TIFF:
  1. Calculates Hamming distance to all JPEG hashes
  2. Selects top K candidates with lowest Hamming distance
  3. If Hamming < threshold, loads images and computes SSIM
  4. Selects best match based on SSIM or Hamming distance
- Creates mapping CSV with match results

**Metrics used:**
- **Hamming Distance:** Fast bitwise comparison between hashes
- **SSIM (Structural Similarity Index):** Precise image similarity measurement (0.0 to 1.0)

**Output:** CSV with columns: `TIFF_file`, `TIFF_path`, `JPEG_file`, `JPEG_path`, `hamming_distance`, `ssim_value`, `used_ssim`


#### `optimized_compare_n_tiff_to_all_jpeg.py`

Optimized version for processing large numbers of TIFFs (potentially all ~10,000).

**What it does:**
- Same matching logic as `compare_n_tiff_to_jpeg.py`
- Uses PyTorch for GPU-accelerated SSIM calculation
- Processes images in batches for memory efficiency
- Significantly faster for large-scale comparisons

**Optimizations:**
- GPU acceleration (CUDA support)
- Batch processing of images
- Normalized image arrays for efficient computation

**Use case:** Production runs with thousands of TIFF files

### `labeling/`

Organize images by category and assign standardized label prefixes.

#### `copy_.and_assign_true_labels.py`

Copies TIFF files and renames them with category labels based on JPEG matches.

**What it does:**
- Reads TIFF→JPEG mapping CSV from comparing scripts
- For each matched pair:
  - Extracts label from JPEG filename (e.g., `L5_` for Particles)
  - Copies original TIFF file to output folder
  - Renames with format: `L{category}{original_filename}.tif`
- Only processes rows where `used_ssim == True` (validated matches)

**Label format:** `L0_` through `L9_` for 10 categories (Biological, Fibres, Films, MEMS, Nanowires, Particles, Patterned, Porous, Powder, Tips)

**Example:**
- Original TIFF: `sample_123.tif`
- Matched JPEG: `L5_abc123def456.jpg`
- Output: `L5_sample_123.tif` (in Particles category)

### `csv/`

Generated CSV files with hashes and mappings (most excluded from repository).

#### `n_tiff_to_all_jpeg_mapping/`

Contains TIFF→JPEG mapping results from comparison scripts.

**Files:**
- `1_tiff.csv`: Single TIFF test mapping
- `100_tiff.csv`: 100 TIFF sample mapping
- `1000_tiff.csv`: 1000 TIFF mapping
- `all_tiff.csv`: Complete dataset mapping (if generated)

## Processing Pipeline

```
1. TIFF Files (original microscopy images)
   ↓
2. create_jpeg_hashes_all_labels.py → CSV with hashes
   ↓
3. compare_n_tiff_to_jpeg.py → CSV with TIFF-JPEG mappings
   ↓
4. copy_.and_assign_true_labels.py → Labeled TIFF files
```

## Key Concepts

### Perceptual Hashing (pHash)

- **Purpose:** Create fingerprints of images that are similar for similar images
- **Algorithm:** Discrete Cosine Transform (DCT) based
- **Hash Size:** 32×32 = 1024 bits
- **Standardization:** Grayscale, histogram equalization, auto-contrast
- **Robustness:** Invariant to minor changes in brightness, contrast, compression

### Image Matching Strategy

**Two-stage approach:**

1. **Stage 1 - Hamming Distance:** Fast comparison of hash fingerprints
   - Counts differing bits between two hashes
   - Threshold < 150 for preliminary matching
   - Computationally cheap, runs on all candidates

2. **Stage 2 - SSIM:** Precise structural similarity (only for promising candidates)
   - Loads actual images into memory
   - Computes structural similarity (0.0 to 1.0)
   - Triggered only when Hamming < 120
   - More accurate but computationally expensive

This approach balances speed and accuracy by filtering with Hamming before applying SSIM.


## Dependencies

All scripts require packages from `../requirement.txt`:

```
Pillow>=10.0.0           # Image processing
imagehash>=4.3.1         # Perceptual hashing
pandas>=2.0.0            # Data management
scikit-image>=0.21.0     # SSIM metrics
numpy>=1.24.0            # Array operations
torch>=2.0.0             # GPU acceleration (optimized scripts)
tqdm>=4.65.0             # Progress bars
```

Install with:
```bash
pip install -r requirement.txt
```

---

**License:** MIT  
**Last Updated:** December 2025
