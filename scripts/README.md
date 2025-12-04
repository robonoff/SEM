# Scripts Folder Documentation

## Overview

This folder contains all Python scripts used for processing, analyzing, and organizing the SEM (Scanning Electron Microscopy) image dataset. The scripts handle the complete pipeline from TIFF-to-JPEG conversion to validation and visualization.

## Folder Structure

```
scripts/
├── jpeg_converter.py           # Main TIFF→JPEG conversion script
├── comparing/                  # Image matching and comparison scripts
├── hashing/                    # Hash generation scripts
├── labeling/                   # Image labeling and organization scripts
├── metadata/                   # Accuracy analysis and validation scripts
├── plots/                      # Visualization and plotting scripts
├── csv/                        # Generated CSV files with hashes and mappings
└── sample_100/                 # Sample/test scripts for prototyping
```

## Main Scripts

### jpeg_converter.py

**Location:** `scripts/jpeg_converter.py`

**Purpose:** Batch conversion of TIFF images to JPEG format with maximum quality preservation.

**Key Features:**
- Recursive directory scanning
- Maintains original directory structure
- 100% JPEG quality setting
- RGB color conversion
- Progress feedback

**Usage:**
```bash
python jpeg_converter.py
# Enter input folder path: /path/to/tiff/folder
# Enter output folder path: /path/to/jpeg/output
```

**Technical Details:**
- Uses PIL/Pillow for image processing
- Handles both `.tif` and `.tiff` extensions
- Converts all images to RGB before saving
- Preserves original filename (changes extension only)

## Subdirectories

### 1. comparing/

Contains scripts for matching JPEG images with their original TIFF counterparts using perceptual hashing and similarity metrics.

#### Files:

**compare.py**
- **Purpose:** Main comparison script that matches JPEG images to original TIFFs
- **Algorithm:**
  1. Computes Hamming distance between pHash values
  2. If Hamming < 120, loads images and calculates SSIM
  3. Selects best match based on SSIM or Hamming distance
- **Metrics:**
  - Hamming distance (on pHash)
  - SSIM (Structural Similarity Index)
- **Output:** CSV with columns: `jpeg_path`, `matched_tiff_path`, `hamming_distance`, `ssim_value`, `used_ssim`

**compare_n_tiff_to_jpeg.py**
- **Purpose:** Direct N-to-N comparison between TIFF and JPEG subsets
- **Use Case:** Small batch validation and testing
- **Features:** Simplified comparison logic for smaller datasets

**optimized_compare_n_tiff_to_all_jpeg.py**
- **Purpose:** Optimized version for comparing N TIFFs with entire JPEG dataset
- **Optimizations:**
  - Parallel computation
  - Batch hash loading
  - Memory-efficient processing
  - Image array caching
- **Use Case:** Large-scale comparisons (1000+ TIFFs)

**Comparison Flow:**
```
TIFF hashes + JPEG hashes
         ↓
   Hamming distance
         ↓
   Threshold check (< 120)
         ↓
   Load images → SSIM
         ↓
   Best match selection
         ↓
   CSV mapping output
```

### 2. hashing/

Scripts for generating perceptual hashes (pHash) of images for similarity comparison.

#### Files:

**create_jpeg_hashes_all_labels.py**
- **Purpose:** Generate pHash for all JPEG images across all categories
- **Hash Type:** Perceptual Hash (pHash)
- **Hash Size:** 32×32 = 1024 bits
- **Image Standardization:**
  1. Convert to grayscale (L mode)
  2. Histogram equalization
  3. Auto-contrast adjustment
- **Output:** `csv/jpeg_hashes_all_labels.csv`
- **Format:** `file`, `path`, `phash`

**create_jpeg_hashes_single_label.py**
- **Purpose:** Generate hashes for a single category/label
- **Use Case:** 
  - Processing individual categories
  - Memory-constrained environments
  - Incremental updates
- **Output:** Category-specific CSV files in `csv/single_label_jpeg_hashes/`
- **Example outputs:**
  - `Biological_complete_jpeg_hashes.csv`
  - `Fibres_complete_jpeg_hashes.csv`
  - `Films_Coated_Surface_complete_jpeg_hashes.csv`

**Technical Details:**
- Uses `imagehash` library (pHash algorithm)
- Standardization ensures consistent hashing
- Robust to minor variations (compression, brightness)
- Generates 64-character hexadecimal hash strings

### 3. labeling/

Scripts for organizing images by category and assigning label prefixes to filenames.

#### Files:

**copy_and_assign_label.py**
- **Purpose:** Copy JPEG images and assign category label prefix
- **Process:**
  1. Read TIFF→JPEG mapping CSV
  2. Identify JPEGs belonging to each category
  3. Copy to destination folder
  4. Rename with label prefix: `L{n}_{hash}.jpg`
- **Label Format:** `L0_` through `L9_` for 10 categories
- **Example:**
  - Original: `abc123def456.jpg`
  - Labeled: `L5_abc123def456.jpg` (Particles category)

**optimized_copy_and_assign_label.py**
- **Purpose:** Optimized version with parallel processing
- **Improvements:**
  - Multi-threading for I/O operations
  - Batch processing
  - Progress bars (tqdm)
  - Error handling and logging
- **Use Case:** Large datasets (10,000+ images)

**copy_.and_assign_true_labels.py**
- **Purpose:** Assign labels based on ground truth or manual validation
- **Use Case:**
  - Validation against manually verified labels
  - Correction of misclassifications
  - Quality assurance checks

**Label Mapping:**
```
L0 → Biological
L1 → Fibres
L2 → Films_Coated_Surface
L3 → MEMS_devices_and_electrodes
L4 → Nanowires
L5 → Particles
L6 → Patterned_surface
L7 → Porous_Sponge
L8 → Powder
L9 → Tips
```

### 4. metadata/

Scripts for analyzing accuracy, validation, and generating statistics reports.

#### Files:

**general_accuracy.py**
- **Purpose:** Calculate overall accuracy of TIFF→JPEG matching
- **Metrics Computed:**
  - Match accuracy percentage
  - Average Hamming distance
  - Average SSIM
  - Distribution statistics (min, max, std dev)
  - Category-wise breakdown
- **Output:** 
  - Text report with summary statistics
  - CSV with detailed metrics
  - Distribution analysis

**excellent_accuracy_check** *(excluded from repository)*
- **Purpose:** Verify matches with excellent SSIM scores
- **Threshold:** SSIM > 0.95
- **Note:** This script/output is not included in the repository (see `.gitignore`)

**compare_accuracy_results.txt**
- **Purpose:** Text file containing accuracy analysis results
- **Content Example:**
  ```
  Total matches: 12000
  Excellent matches (SSIM > 0.95): 11500 (95.83%)
  Average SSIM: 0.978
  Average Hamming: 8.34
  ```

**Analysis Output:**
- Statistical summaries
- Quality metrics
- Error identification
- Validation reports

### 5. plots/

Visualization scripts for generating histograms and plots of similarity metrics.

#### Files:

**hamming_histogram.py**
- **Purpose:** Generate histogram of Hamming distances
- **Output:** `hamming_histogram_logscale.png`
- **Features:**
  - Logarithmic Y-axis for better visibility
  - Distribution visualization
  - Threshold indicators
  - Statistical annotations

**ssim_histogram.py**
- **Purpose:** Generate SSIM distribution histograms
- **Output:**
  - `ssim_histogram.png` (linear scale)
  - `ssim_histogram_logscale.png` (log scale)
- **Features:**
  - Bins: 0.0 - 1.0 with 0.05 step
  - Highlights SSIM > 0.95 threshold
  - Color-coded quality regions

**ssim_plot_by_row.py**
- **Purpose:** Plot SSIM values for each individual match
- **Output:** `ssim_plot_by_row.png`
- **Features:**
  - X-axis: Match index
  - Y-axis: SSIM value
  - Identifies outliers
  - Highlights problematic matches
- **Use Case:** Debugging individual match quality

**Visualization Types:**
```
Hamming Histogram:
- Shows distribution of hash distances
- Identifies typical match ranges
- Highlights anomalies

SSIM Histogram:
- Quality distribution overview
- Success rate visualization
- Threshold validation

SSIM by Row:
- Individual match inspection
- Outlier detection
- Sequential quality tracking
```


## DATA

### 6. csv/

Contains all generated CSV files with hashes, mappings, and analysis results.

#### Structure:

```
csv/
├── jpeg_hashes_all_labels.csv          # All JPEG pHashes
├── tiff_hashes.csv                     # All TIFF pHashes
├── jpeg_hashes_test_tiff_to_jpeg.csv   # Test JPEG hashes
├── tiff_hashes_test_tiff_to_jpeg.csv   # Test TIFF hashes
├── n_tiff_to_all_jpeg_mapping/         # N TIFF → all JPEG mappings
│   ├── 1_tiff.csv
│   ├── 100_tiff.csv
│   └── 1000_tiff.csv
├── n_tiff_to_single_label_jpeg_mapping/ # Per-category mappings
│   ├── Biological_all_tiff_to_jpeg_mapping.csv
│   ├── Fibres_all_tiff_to_jpeg_mapping.csv
│   └── [other categories]...
├── single_label_jpeg_hashes/           # Per-category hash files
│   └── [category]_complete_jpeg_hashes.csv
├── sample_100/                         # Sample dataset CSVs
│   └── [test files for 100-image samples]
└── old/                                # Deprecated CSV files
```

#### CSV File Formats:

**Hash CSV Format:**
```csv
file,path,phash
image.jpg,/full/path/to/image.jpg,abc123def456789...
```

**Mapping CSV Format:**
```csv
jpeg_path,matched_tiff_path,hamming_distance,ssim_value,used_ssim
/path/jpeg.jpg,/path/tiff.tif,5,0.987,True
```

### 7. sample_100/

Contains scripts for testing and prototyping with sample datasets (100 images per category).

#### Purpose:
- **Algorithm validation** before full-scale processing
- **Quick testing** of new features
- **Performance benchmarking**
- **Prototyping** new comparison methods

#### Files:

**create_jpeg_hashes_sample.py**
- Creates hashes for 100-image samples per category
- Faster execution for development
- Outputs to `csv/sample_100/`

#### Output Format:
```
sample_100/
├── {label}_jpeg_tiff_hashing.csv        # JPEG hashes
└── {label}_jpeg_tiff_hashing_mapping.csv # Mapping results
```

## Workflow Integration

### Complete Pipeline:

```
1. CONVERSION
   jpeg_converter.py
   ├─ Input: backup_folder/ (TIFFs)
   └─ Output: JPEG files

2. HASHING
   hashing/create_jpeg_hashes_all_labels.py
   ├─ Input: JPEG files
   └─ Output: csv/jpeg_hashes_all_labels.csv

3. COMPARISON
   comparing/compare.py
   ├─ Input: JPEG hashes + TIFF hashes
   └─ Output: csv/mapping.csv

4. LABELING
   labeling/copy_and_assign_label.py
   ├─ Input: Mapping CSV
   └─ Output: Labeled JPEG files (L{n}_*.jpg)

5. VALIDATION
   metadata/general_accuracy.py
   ├─ Input: Mapping CSV
   └─ Output: Accuracy reports

6. VISUALIZATION
   plots/[histogram scripts]
   ├─ Input: Mapping CSV
   └─ Output: PNG plots
```

## Technical Requirements

### Dependencies:

All scripts require the following Python packages (see `../requirement.txt`):

```
Pillow>=10.0.0           # Image manipulation
imagehash>=4.3.1         # Perceptual hashing
pandas>=2.0.0            # CSV data management
tqdm>=4.65.0             # Progress bars
scikit-image>=0.21.0     # SSIM and image metrics
numpy>=1.24.0            # Array operations
matplotlib>=3.7.0        # Plotting (for visualization scripts)
```

### Python Version:
- **Minimum:** Python 3.8+
- **Recommended:** Python 3.10+

## Usage Guidelines

### For New Users:

1. **Start with samples:**
   ```bash
   cd sample_100/
   python create_jpeg_hashes_sample.py
   ```

2. **Test conversion:**
   ```bash
   python jpeg_converter.py
   # Use small test folder first
   ```

3. **Generate hashes:**
   ```bash
   cd hashing/
   python create_jpeg_hashes_single_label.py
   # Process one category first
   ```

4. **Run comparison:**
   ```bash
   cd comparing/
   python compare.py
   # Check results in csv/ folder
   ```

### For Production:

1. Use **optimized versions** for large datasets
2. Process **by category** to manage memory
3. Enable **progress bars** (tqdm) for monitoring
4. Check **accuracy reports** after each major step

### Performance Tips:

- **Batch Processing:** Use `optimized_*` scripts for >1000 images
- **Memory Management:** Process categories separately
- **I/O Optimization:** SSD recommended for large datasets
- **CPU Usage:** Scripts benefit from multi-threading (4+ cores)

## Common Tasks

### Add New Images:

```bash
# 1. Convert TIFFs
python jpeg_converter.py

# 2. Generate hashes
cd hashing/
python create_jpeg_hashes_all_labels.py

# 3. Compare and map
cd ../comparing/
python compare.py

# 4. Assign labels
cd ../labeling/
python copy_and_assign_label.py

# 5. Validate
cd ../metadata/
python general_accuracy.py
```

### Validate Specific Category:

```bash
# Generate hashes for single category
cd hashing/
python create_jpeg_hashes_single_label.py
# Select category when prompted

# Check accuracy
cd ../metadata/
python general_accuracy.py
```

### Generate Reports:

```bash
# Create all visualizations
cd plots/
python hamming_histogram.py
python ssim_histogram.py
python ssim_plot_by_row.py

# Outputs saved in plots/ folder
```

## File Paths

Scripts use absolute paths configured at the top of each file. Update these paths according to your environment:

```python
# Example from create_jpeg_hashes_all_labels.py
jpeg_root = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/public_dataset/Complete_dataset"
output_csv = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/jpeg_hashes_all_labels.csv"
```

**Configuration locations:**
- Input/output folders: Top of each script
- CSV paths: Usually in `BASE_DIR` variable
- Dataset paths: In `jpeg_root`, `tiff_root`, etc.

## Troubleshooting

### Common Issues:

**"File not found" errors:**
- Check and update absolute paths in script headers
- Verify input folder exists and contains expected files

**"Out of memory" errors:**
- Process by category instead of all at once
- Use sample scripts for testing
- Reduce batch size in optimized scripts

**Low SSIM values:**
- Verify images are properly standardized
- Check for resolution mismatches
- Use visualization scripts to identify problematic matches

**Slow performance:**
- Use optimized versions of scripts
- Ensure SSD storage for I/O operations
- Check CPU/memory usage

### Debug Mode:

Most scripts include progress bars and print statements. To enable verbose output:

```python
# Add at top of script
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new scripts:

1. **Follow naming convention:** `verb_noun.py` or `optimized_verb_noun.py`
2. **Add docstrings:** Explain purpose, inputs, outputs
3. **Update this README:** Document new functionality
4. **Test with samples:** Use `sample_100/` for validation
5. **Update dependencies:** Add to `requirement.txt` if needed

## Additional Resources

- **Main Documentation:** See `../DOCUMENTATION.md` for complete project overview
- **Dataset Paper:** See `../sem_dataset_paper.pdf` for scientific background
- **Folder Structure:** See `../output.txt` for complete file tree

---

**Last Updated:** December 2025  
**Version:** 1.0  
**Maintained by:** SEM Dataset Project Team
