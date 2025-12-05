# Scripts Documentation

## Overview

This folder contains all Python scripts for processing and analyzing the SEM dataset. The scripts are organized by function into subdirectories, handling everything from TIFF-to-JPEG conversion to validation and visualization.

## Directory Structure

```
scripts/
├── jpeg_converter.py           # Main conversion script
├── comparing/                  # Image matching scripts
│   ├── compare.py
│   ├── compare_n_tiff_to_jpeg.py
│   └── optimized_compare_n_tiff_to_all_jpeg.py
├── hashing/                    # Hash generation scripts
│   ├── create_jpeg_hashes_all_labels.py
│   └── create_jpeg_hashes_single_label.py
├── labeling/                   # Image labeling scripts
│   ├── copy_and_assign_label.py
│   ├── optimized_copy_and_assign_label.py
│   └── copy_.and_assign_true_labels.py
├── metadata/                   # Accuracy analysis scripts
│   ├── general_accuracy.py
│   ├── excellent_accuracy_check.py
│   └── compare_accuracy_results.txt
├── plots/                      # Visualization scripts
│   ├── hamming_histogram.py
│   ├── ssim_histogram.py
│   └── ssim_plot_by_row.py
├── csv/                        # Generated CSV data files
│   ├── n_tiff_to_all_jpeg_mapping/
│   └── sample_100/
└── sample_100/                 # Sample/test scripts
```

> **Note**: Some files and directories are excluded from version control (see `.gitignore`). Generated CSV files will appear in `csv/` when you run the scripts.

## Main Conversion Script

### jpeg_converter.py

**Location**: `scripts/jpeg_converter.py`

**Purpose**: Batch converts TIFF images to JPEG format with maximum quality preservation.

**What it does**:
1. Recursively scans input folder for all `.tif` and `.tiff` files
2. Opens each TIFF file using PIL/Pillow
3. Converts to RGB color space
4. Saves as JPEG with 100% quality setting
5. Maintains original directory structure in output folder

**Usage**:
```bash
python jpeg_converter.py
```
The script will prompt you for:
- Input folder path (where TIFF files are located)
- Output folder path (where to save converted JPEGs)

**Technical details**:
- Uses Pillow (PIL) for image processing
- Handles both `.tif` and `.tiff` extensions
- Preserves original filename (changes extension only)
- No image manipulation or resizing

## Hashing Scripts

### Directory: `hashing/`

These scripts generate perceptual hashes (pHash) for images to enable similarity matching.

#### create_jpeg_hashes_all_labels.py

**Purpose**: Generates pHash for all JPEG images across all categories in the dataset.

**What it does**:
1. Recursively finds all JPEG files in the specified directory
2. For each image:
   - Loads the image
   - Applies standardization (grayscale conversion, histogram equalization, auto-contrast)
   - Computes perceptual hash using pHash algorithm (32×32 hash size)
   - Stores hash as 64-character hexadecimal string
3. Saves all hashes to a CSV file with columns: `file`, `path`, `phash`

**Image standardization pipeline**:
```python
1. Convert to grayscale (L mode)
2. Apply histogram equalization
3. Apply auto-contrast adjustment
4. Compute pHash (32×32 = 1024 bits)
```

**Output**: `csv/jpeg_hashes_all_labels.csv`

**Why standardization?**: Ensures consistent hashing regardless of minor variations in brightness, contrast, or color balance.

#### create_jpeg_hashes_single_label.py

**Purpose**: Generates pHash for images belonging to a single category/label.

**What it does**:
- Same process as `create_jpeg_hashes_all_labels.py`
- Processes only one category at a time
- Useful for memory-constrained environments or incremental processing

**Output**: Category-specific CSV files in `csv/single_label_jpeg_hashes/`
- Example: `Biological_complete_jpeg_hashes.csv`, `Fibres_complete_jpeg_hashes.csv`, etc.

## Comparing Scripts

### Directory: `comparing/`

These scripts match JPEG images with their original TIFF counterparts using perceptual hashing and similarity metrics.

#### compare.py

**Purpose**: Main comparison script that matches JPEG images to original TIFFs using a two-stage approach.

**What it does**:
1. Loads pHash values for both JPEG and TIFF images from CSV files
2. For each JPEG image:
   - **Stage 1**: Computes Hamming distance between JPEG hash and all TIFF hashes
   - **Stage 2**: If Hamming distance < 120, loads actual images and computes SSIM (Structural Similarity Index)
   - Selects best match based on SSIM (if calculated) or minimum Hamming distance
3. Creates a mapping CSV with match results

**Metrics used**:
- **Hamming Distance**: Number of differing bits between two hashes
  - Fast to compute (bitwise XOR operation)
  - Threshold: < 150 for preliminary matching, < 120 for SSIM trigger
- **SSIM (Structural Similarity Index)**: Measures structural similarity between images
  - Range: 0.0 (completely different) to 1.0 (identical)
  - More accurate than Hamming distance but computationally expensive
  - Used for final decision when Hamming < 120

**Algorithm flow**:
```
For each JPEG:
  ├─ Calculate Hamming distance with all TIFFs
  ├─ Find minimum Hamming distance
  ├─ If Hamming < 120:
  │   ├─ Load JPEG image into memory
  │   ├─ Load candidate TIFF images
  │   ├─ Compute SSIM for each candidate
  │   └─ Select match with highest SSIM
  └─ Else:
      └─ Select match with lowest Hamming distance
```

**Output CSV columns**:
- `jpeg_path`: Full path to JPEG file
- `matched_tiff_path`: Full path to matched TIFF file
- `hamming_distance`: Hamming distance between hashes
- `ssim_value`: SSIM value (if calculated, else 0)
- `used_ssim`: Boolean indicating if SSIM was used for matching

#### compare_n_tiff_to_jpeg.py

**Purpose**: Direct N-to-N comparison between TIFF and JPEG subsets.

**What it does**:
- Simplified version for comparing a specific subset of TIFFs with a subset of JPEGs
- Used for validation and testing with smaller datasets
- Same two-stage matching approach as `compare.py`

**Use case**: Testing algorithm accuracy on sample datasets before full-scale processing.

#### optimized_compare_n_tiff_to_all_jpeg.py

**Purpose**: Optimized version for comparing N TIFFs with the entire JPEG dataset.

**What it does**:
- Same matching logic as `compare.py`
- Optimizations:
  - Batch loading of hashes to reduce I/O
  - Parallel computation using multi-threading
  - Image array caching to avoid redundant loading
  - Memory-efficient processing of large datasets

**Use case**: Processing 1000+ TIFFs against the full JPEG dataset (10,000+ images).

**When to use**: 
- `compare.py`: Standard processing, moderate dataset size
- `compare_n_tiff_to_jpeg.py`: Small validation samples
- `optimized_compare_n_tiff_to_all_jpeg.py`: Large-scale production runs

## Labeling Scripts

### Directory: `labeling/`

These scripts organize images by category and assign standardized label prefixes to filenames.

#### copy_and_assign_label.py

**Purpose**: Copies JPEG images and renames them with category label prefixes.

**What it does**:
1. Reads TIFF→JPEG mapping CSV file
2. For each mapped pair:
   - Extracts label from JPEG filename (first 3 characters: `L0_`, `L1_`, etc.)
   - Copies TIFF file to destination folder
   - Renames with format: `L{category_number}{original_filename}.tif`
3. Organizes labeled files by category

**Label mapping**:
```
L0_ → Biological
L1_ → Fibres
L2_ → Films_Coated_Surface
L3_ → MEMS_devices_and_electrodes
L4_ → Nanowires
L5_ → Particles
L6_ → Patterned_surface
L7_ → Porous_Sponge
L8_ → Powder
L9_ → Tips
```

**Example transformation**:
```
Original TIFF: sample_123.tif
Matched JPEG: L5_abc123def456.jpg
Result: L5_sample_123.tif (in Particles category)
```

#### optimized_copy_and_assign_label.py

**Purpose**: Parallelized version for faster processing of large datasets.

**What it does**:
- Same functionality as `copy_and_assign_label.py`
- Improvements:
  - Multi-threading for concurrent I/O operations
  - Batch processing to reduce overhead
  - Progress bars (tqdm) for monitoring
  - Better error handling and logging

**Use case**: Processing 10,000+ images where speed is critical.

#### copy_.and_assign_true_labels.py

**Purpose**: Assigns labels based on ground truth or manually verified data.

**What it does**:
- Reads mapping from manually curated or validated label assignments
- Used for quality assurance and validation against known-correct labels
- Helps identify misclassifications from automated matching

**Use case**: Validation and correction of automated labeling results.

## Metadata Scripts

### Directory: `metadata/`

These scripts analyze accuracy, generate statistics, and validate matching quality.

#### general_accuracy.py

**Purpose**: Calculates comprehensive accuracy metrics for TIFF→JPEG matching.

**What it does**:
1. Reads matching results from CSV files
2. Computes statistics:
   - **Match accuracy**: Percentage of correctly mapped images
   - **Mean Hamming distance**: Average hash distance
   - **Mean SSIM**: Average structural similarity
   - **Distribution statistics**: Min, max, standard deviation
   - **Category-wise breakdown**: Per-label accuracy metrics
3. Generates text report and detailed CSV

**Metrics calculated**:
- Total number of matches
- Excellent matches (SSIM > 0.95)
- Good matches (SSIM 0.85-0.95)
- Acceptable matches (SSIM 0.70-0.85)
- Problematic matches (SSIM < 0.70)
- Mean, median, std dev for Hamming and SSIM

**Output**: 
- Text report with summary
- CSV with detailed match statistics
- Per-category analysis

#### excellent_accuracy_check.py

**Purpose**: Identifies and analyzes matches with excellent SSIM scores.

**What it does**:
1. Filters matches with SSIM > 0.95
2. Calculates percentage of excellent matches
3. Analyzes distribution by category
4. Identifies outliers and potential issues

**Use case**: Quality assurance - verifying that the vast majority of matches are high-quality.

**Output**:
- List of excellent matches
- Percentage by category
- Identification of categories with lower accuracy

#### compare_accuracy_results.txt

**Purpose**: Pre-generated text file with accuracy analysis results.

**Content example**:
```
Total matches: 12000
Excellent matches (SSIM > 0.95): 11500 (95.83%)
Average SSIM: 0.978
Average Hamming: 8.34
Min SSIM: 0.832
Max SSIM: 1.000
```

## Plots Scripts

### Directory: `plots/`

These scripts generate visualizations for quality assessment and analysis.

#### hamming_histogram.py

**Purpose**: Generates histogram of Hamming distances across all matches.

**What it does**:
1. Reads Hamming distances from matching CSV
2. Creates histogram showing distribution
3. Uses logarithmic Y-axis for better visibility
4. Adds statistical annotations (mean, median, thresholds)

**Output**: `hamming_histogram_logscale.png`

**Interpretation**:
- Low Hamming distances (0-50): Very similar images, high confidence matches
- Medium distances (50-120): Similar images, SSIM validation recommended
- High distances (>120): Different images, likely mismatches

#### ssim_histogram.py

**Purpose**: Generates histograms of SSIM values across all matches.

**What it does**:
1. Reads SSIM values from matching CSV
2. Creates two versions:
   - Linear scale histogram
   - Logarithmic scale histogram
3. Highlights quality thresholds (0.95, 0.85, 0.70)
4. Color-codes quality regions

**Output**:
- `ssim_histogram.png` (linear scale)
- `ssim_histogram_logscale.png` (log scale)

**Features**:
- Bins: 0.0 to 1.0 with 0.05 step size
- Quality threshold markers
- Statistical annotations

**Interpretation**:
- Peak near 1.0: Most matches are excellent quality
- Long tail: Some lower-quality matches to investigate
- Bimodal distribution: May indicate two classes of matches

#### ssim_plot_by_row.py

**Purpose**: Plots SSIM values for each individual match sequentially.

**What it does**:
1. Reads matches in order from CSV
2. Plots SSIM value for each match
3. Highlights outliers (SSIM < 0.85)
4. Shows trends and patterns across dataset

**Output**: `ssim_plot_by_row.png`

**Features**:
- X-axis: Match index (1 to N)
- Y-axis: SSIM value (0.0 to 1.0)
- Horizontal lines for quality thresholds
- Different colors for quality levels

**Use case**: 
- Identifying specific problematic matches
- Detecting patterns in match quality
- Finding categories with systematic issues
- Debugging matching algorithm

## CSV Data Files

### Directory: `csv/`

Contains generated CSV files with hashes, mappings, and results.

**Structure**:
```
csv/
├── n_tiff_to_all_jpeg_mapping/    # Mapping results (included in repo)
│   ├── 1_tiff.csv                 # 1 TIFF mapped to JPEG dataset
│   ├── 100_tiff.csv               # 100 TIFFs mapped
│   └── 1000_tiff.csv              # 1000 TIFFs mapped
└── sample_100/                    # Sample dataset results
```

**Excluded from repository** (generated when scripts run):
- `jpeg_hashes_all_labels.csv`: All JPEG pHashes
- `tiff_hashes.csv`: All TIFF pHashes  
- `single_label_jpeg_hashes/`: Per-category hash files
- Other generated mapping files

**CSV formats**:

**Hash CSV**:
```csv
file,path,phash
image.jpg,/full/path/to/image.jpg,abc123def456...
```

**Mapping CSV**:
```csv
jpeg_path,matched_tiff_path,hamming_distance,ssim_value,used_ssim
/path/jpeg.jpg,/path/tiff.tif,5,0.987,True
```

## Sample Scripts

### Directory: `sample_100/`

Contains scripts for testing with sample datasets (100 images per category).

**Purpose**:
- Algorithm validation before full-scale processing
- Quick testing of new features
- Performance benchmarking
- Prototyping modifications

**Files**: Similar to main scripts but configured for smaller datasets.

## Complete Workflow

### Standard Processing Pipeline

```bash
# 1. Convert TIFF to JPEG
cd /path/to/SEM/scripts
python jpeg_converter.py

# 2. Generate hashes for all JPEGs
cd hashing
python create_jpeg_hashes_all_labels.py

# 3. Match JPEGs to TIFFs
cd ../comparing
python compare.py

# 4. Assign category labels
cd ../labeling
python copy_and_assign_label.py

# 5. Validate accuracy
cd ../metadata
python general_accuracy.py

# 6. Generate visualizations
cd ../plots
python hamming_histogram.py
python ssim_histogram.py
python ssim_plot_by_row.py
```

### For Large Datasets

```bash
# Use optimized versions
cd comparing
python optimized_compare_n_tiff_to_all_jpeg.py

cd ../labeling
python optimized_copy_and_assign_label.py
```

### For Testing

```bash
# Use sample scripts
cd sample_100
python create_jpeg_hashes_sample.py
# ... test with smaller dataset
```

## Configuration

Most scripts use absolute paths defined at the top of each file. Before running, update these paths to match your environment:

```python
# Example from create_jpeg_hashes_all_labels.py
jpeg_root = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/public_dataset/Complete_dataset"
output_csv = "/orfeo/cephfs/scratch/mdmc/appliedAI/SEM/scripts/csv/jpeg_hashes_all_labels.csv"
```

**Configuration locations**:
- Input/output folders: Top of each script
- CSV paths: Usually in `BASE_DIR` variable
- Dataset paths: `jpeg_root`, `tiff_root`, etc.

## Dependencies

All scripts require packages listed in `../requirement.txt`:

```
Pillow>=10.0.0           # Image manipulation
imagehash>=4.3.1         # Perceptual hashing
pandas>=2.0.0            # CSV data management
tqdm>=4.65.0             # Progress bars
scikit-image>=0.21.0     # SSIM metrics
numpy>=1.24.0            # Array operations
matplotlib>=3.7.0        # Plotting
```

Install with:
```bash
pip install -r requirement.txt
```

## Performance Tips

- **Memory Management**: Process categories separately for large datasets
- **Batch Processing**: Use `optimized_*` scripts for >1000 images
- **I/O Optimization**: SSD storage recommended
- **CPU Usage**: Scripts benefit from multi-threading (4+ cores recommended)
- **Testing**: Always test with sample datasets before full runs

## Troubleshooting

**"File not found" errors**:
- Update absolute paths in script headers
- Verify input folders exist

**"Out of memory" errors**:
- Process by category instead of all at once
- Use `sample_100/` scripts for testing
- Reduce batch size in optimized scripts

**Low SSIM values**:
- Check image standardization
- Verify resolution compatibility
- Use visualization scripts to identify issues

**Slow performance**:
- Use optimized script versions
- Ensure SSD storage
- Check CPU/memory usage

For more information, see the main [repository README](../README.md).

---

**Last Updated**: December 2025  
**Python Version**: 3.8+ (3.10+ recommended)  
**Maintainer**: Roberta Lamberti
