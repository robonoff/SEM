# SEM Dataset Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Dataset](#dataset)
4. [Scripts](#scripts)
5. [Project Workflow](#project-workflow)
6. [Dependencies](#dependencies)
7. [Results and Output](#results-and-output)

## Project Overview

This project manages, converts, and analyzes a SEM (Scanning Electron Microscopy) image dataset. The main objectives are:

1. **Convert TIFF images to JPEG** to create a public dataset
2. **Create image hashes** to uniquely identify each file
3. **Map relationships** between original TIFF images and converted JPEGs
4. **Validate conversion accuracy** through similarity metrics
5. **Organize images by scientific categories** (labels)



## Folder Structure

### Main Directory

```
/home/robertalamberti/SEM/
├── backup_folder/          # Original TIFF dataset organized by researchers
├── jpeg_conversion_test/   # JPEG conversion tests
├── labeled_tif/             # Python scripts for processing
├── scripts/                
├── public_dataset          # compressed datasets
├── requirement.txt         # Python dependencies
└── sem_dataset_paper.pdf   # Scientific documentation
```

### backup_folder

Contains **981 directories** organized by researcher, with a total of **~38,000 TIFF files**. Each researcher has their own folder with subfolders organized by date or experiment. It's the original folder provided by the lecturer.

**Example structure:**
```
backup_folder/
├── Cassese D/
│   └── GaAs_NWs/
│       └── 2013-02-19/
│           └── G031c_100h_b_05.tif
├── Dalmiglio M/
│   ├── 02-03-09/
│   ├── 03-04-08/
│   └── ...
├── DanieleB/
│   ├── biotin nps/
│   ├── capped pillars/
│   └── ...
└── [other researchers]/
```

**Main researchers:** Cassese D, Dalmiglio M, Dal Zilio S, DanieleB, denis, elena, elvio, flavio, Fraleoni A, GDS, Giorgis V, GiovanniDS, giulio, Giusy, Greco S M L, Gregoratti, Grenci G, grubi, hossein, ILO, Istem, Jashmini, Jeromy, John, Konstantin, labmodesti, Lazzarino M, Leonardo, Lorenzo D, lucab, luca_p, MariaManna, marina, Marina C, Matteucci M, Melli M, Migliorini E, Mirta, Nappini S, Naumenko, Nicolas, Orru M, Pozzato A, Rago I, Sammito D, vince.

### jpeg_conversion_test

Directory for conversion tests, contains JPEG sample images for validation:

```
jpeg_conversion_test/
└── labeled_images_100/
    ├── Biological/
    ├── Fibres/
    ├── Films_Coated_Surface/
    ├── MEMS_devices_and_electrodes/
    ├── Nanowires/
    ├── Particles/
    ├── Patterned_surface/
    ├── Porous_Sponge/
    ├── Powder/
    └── Tips/
```

Each category contains images with label prefix (e.g., `L0_`, `L1_`, `L2_`, `L3_`  etc.).



## Dataset

### Categories (Labels)

The dataset is organized into **10 scientific categories**:

1. **Biological** (L0) - Biological samples
2. **Fibres** (L1) - Fibers and fibrous structures
3. **Films_Coated_Surface** (L2) - Films and coated surfaces
4. **MEMS_devices_and_electrodes** (L3) - MEMS devices and electrodes
5. **Nanowires** (L4) - Nanowires
6. **Particles** (L5) - Particles
7. **Patterned_surface** (L6) - Patterned surfaces
8. **Porous_Sponge** (L7) - Porous materials and sponges
9. **Powder** (L8) - Powders
10. **Tips** (L9) - Tips (for AFM/microscopy)

### File Formats

- **Original format:** TIFF (.tif/.tiff) - High quality, lossless
- **Public format:** JPEG (.jpg/.jpeg) - Converted with 100% quality
- **Standardization:** All images are converted to grayscale (L), equalized, and auto-contrasted

### Naming Convention

**JPEG with label:**
```
L{label_number}_{hash}.jpg
```
Examples:
- `L5_001eb7a9c7c13bda29f79ee18c84a43e.jpg` (Particles)
- `L0_00ba59bffe72a8b6a61ebae80fcfcf1d.jpg` (Biological)



## Scripts

### Scripts Directory Structure

```
scripts/
├── comparing/              # Comparison and matching scripts
├── csv/                    # CSV files with hashes and mappings
├── hashing/               # Hash generation scripts
├── labeling/              # Labeling and copying scripts
├── metadata/              # Accuracy analysis scripts
├── plots/                 # Visualization scripts
├── sample_100/            # Test sample scripts
├── old_scripts/           # Deprecated scripts
└── jpeg_converter.py      # Main TIFF→JPEG converter
```

### Main Scripts

#### 1. jpeg_converter.py

**Function:** Batch conversion from TIFF to JPEG

**Input:**
- Folder with TIFF files (accepts recursive subfolders)

**Output:**
- JPEG files converted with 100% quality

**Process:**
```python
1. Recursive scanning of input folder
2. For each .tif/.tiff file:
   - Open with PIL
   - Convert to RGB
   - Save as JPEG with 100% quality
```

**Usage:**
```bash
python scripts/jpeg_converter.py
# Enter input folder path
# Enter output folder path
```

#### 2. Hashing Scripts

##### create_jpeg_hashes_all_labels.py

**Function:** Creates perceptual hashes (pHash) for all JPEG images in the complete dataset

**Features:**
- **Algorithm:** Perceptual Hash (pHash) with size 32
- **Standardization:**
  - Convert to grayscale
  - Histogram equalization
  - Auto-contrast

**Output:** `jpeg_hashes_all_labels.csv`
```csv
file,path,phash
L5_001eb7a9c7c13bda29f79ee18c84a43e.jpg,/path/to/file,8f8f8f8f8f8f8f8f
```

##### create_jpeg_hashes_single_label.py

**Function:** Creates hashes for a single category/label

**Output:** Separate CSV files per label in `csv/single_label_jpeg_hashes/`
- `Biological_complete_jpeg_hashes.csv`
- `Fibres_complete_jpeg_hashes.csv`
- `Films_Coated_Surface_complete_jpeg_hashes.csv`
- ... (one for each category)

#### 3. Comparing Scripts

##### compare.py

**Function:** Compares and maps JPEG images with corresponding original TIFFs

**Metrics used:**
1. **Hamming Distance** (on pHash)
   - Threshold: 150 for preliminary matching
   - Threshold: 120 for triggering SSIM
   
2. **SSIM (Structural Similarity Index)**
   - Used for final matching when Hamming < 120
   - Range: 0-1 (1 = identical)

**Algorithm:**
```python
For each JPEG image:
    1. Calculate Hamming distance with all TIFFs
    2. If Hamming < 120:
        a. Load images into memory
        b. Calculate SSIM
        c. Use SSIM as matching criterion
    3. Otherwise:
        a. Use minimum Hamming distance
    4. Save best match
```

**Output:**
- CSV with JPEG → TIFF mapping
- Columns: jpeg_path, matched_tiff_path, hamming_distance, ssim_value

##### optimized_compare_n_tiff_to_all_jpeg.py

**Function:** Optimized version for comparing N TIFF files with entire JPEG dataset

**Optimizations:**
- Batch loading of hashes
- Parallel computation
- Image array caching

##### compare_n_tiff_to_jpeg.py

**Function:** Direct N-to-N comparison between TIFF and JPEG subsets

#### 4. Labeling Scripts

##### copy_and_assign_label.py

**Function:** Copies JPEG images and assigns label in filename

**Process:**
```python
1. Read TIFF→JPEG mapping from CSV
2. For each category:
    a. Identify JPEGs belonging to category
    b. Copy to destination folder
    c. Rename with label prefix: L{n}_{hash}.jpg
```

##### optimized_copy_and_assign_label.py

**Function:** Optimized version with parallelization

**Improvements:**
- Threading for parallel I/O
- Batch processing
- Progress bar with tqdm

##### copy_and_assign_true_labels.py

**Function:** Assigns "true" labels based on manual ground truth or metadata


#### 5. Metadata Scripts

##### general_accuracy.py

**Function:** Calculates general accuracy of TIFF→JPEG matching

**Metrics calculated:**
- **Match accuracy:** % of correctly mapped JPEGs
- **Average Hamming distance:** Mean of Hamming distances
- **Average SSIM:** Mean SSIM for matches with SSIM > 0
- **Distribution statistics:** Min, Max, Std Dev

**Output:** Text report and CSV with statistics

##### excellent_accuracy_check.py

**Function:** Verifies matches with "excellent" SSIM (> 0.95)

**Output:**
- List of matches with SSIM > 0.95
- Percentage of excellent matches
- Analysis by category

##### compare_accuracy_results.txt

Text file with accuracy analysis results:
```
Total matches: 12000
Excellent matches (SSIM > 0.95): 11500 (95.83%)
Average SSIM: 0.978
Average Hamming: 8.34
```


#### 6. Plots Scripts

##### hamming_histogram.py

**Function:** Generates histogram of Hamming distances

**Output:** `hamming_histogram_logscale.png`
- X-axis: Hamming distance
- Y-axis: Frequency (logarithmic scale)
- Shows similarity distribution between images

##### ssim_histogram.py

**Function:** Generates SSIM histograms

**Output:**
- `ssim_histogram.png` (linear scale)
- `ssim_histogram_logscale.png` (logarithmic scale)

**Features:**
- Bins: 0.0 - 1.0 with 0.05 step
- Highlights SSIM > 0.95 threshold

##### ssim_plot_by_row.py

**Function:** SSIM plot for each individual match

**Output:** `ssim_plot_by_row.png`
- X-axis: Match index
- Y-axis: SSIM value
- Identifies outliers and problematic matches


#### 7. Sample Scripts (sample_100/)

##### create_jpeg_hashes_sample.py

**Function:** Creates hashes for sample of 100 images per category

**Usage:**
- Quick tests
- Algorithm validation
- Prototyping

**Output:** CSV in `csv/sample_100/`
- `{label}_jpeg_tiff_hashing.csv` - JPEG hashes
- `{label}_jpeg_tiff_hashing_mapping.csv` - JPEG→TIFF mapping



### Old Scripts (old_scripts/)

Deprecated scripts kept for reference:
- `many_many_rob.py`
- `many_rob.py`
- `prova_sample.py`
- `sample_rob.py`

⚠️ **Do not use:** Replaced by optimized versions


## CSV Files

### CSV Directory Structure

```
csv/
├── jpeg_hashes_all_labels.csv          # All JPEG hashes
├── tiff_hashes.csv                     # All TIFF hashes
├── jpeg_hashes_test_tiff_to_jpeg.csv   # Test hashes
├── tiff_hashes_test_tiff_to_jpeg.csv   # TIFF test hashes
├── n_tiff_to_all_jpeg_mapping/         # N TIFF → all JPEG mapping
├── n_tiff_to_single_label_jpeg_mapping/ # Single label mapping
├── single_label_jpeg_hashes/           # Single label hashes
├── sample_100/                         # Test sample CSVs
└── old/                                # Obsolete CSVs
```

### Main CSV Format

#### jpeg_hashes_all_labels.csv
```csv
file,path,phash
L5_001eb7a9.jpg,/path/to/file,abc123def456...
```

#### TIFF→JPEG Mapping
```csv
jpeg_path,matched_tiff_path,hamming_distance,ssim_value,used_ssim
/path/jpeg.jpg,/path/tiff.tif,5,0.987,True
```

**Columns:**
- `jpeg_path` - Complete JPEG file path
- `matched_tiff_path` - Corresponding TIFF path
- `hamming_distance` - Hamming distance between hashes
- `ssim_value` - SSIM value (if calculated)
- `used_ssim` - Boolean, True if SSIM was used for matching


## Project Workflow

### Phase 1: Dataset Preparation

```
┌─────────────────────┐
│  backup_folder/     │
│  (Original TIFFs)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ jpeg_converter.py   │
│ (Conversion)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  JPEG Dataset       │
└─────────────────────┘
```

### Phase 2: Hashing and Mapping

```
┌─────────────────────────────────────┐
│  JPEG Dataset        TIFF Dataset   │
└────────┬─────────────────┬──────────┘
         │                 │
         ▼                 ▼
┌──────────────┐  ┌──────────────┐
│ Hash JPEG    │  │ Hash TIFF    │
│ (pHash 32)   │  │ (pHash 32)   │
└──────┬───────┘  └──────┬───────┘
       │                 │
       └────────┬────────┘
                ▼
        ┌──────────────┐
        │  compare.py  │
        │  (Matching)  │
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │  Mapping CSV │
        └──────────────┘
```

### Phase 3: Labeling and Organization

```
┌────────────────┐
│  Mapping CSV   │
└────────┬───────┘
         │
         ▼
┌────────────────────┐
│ copy_and_assign    │
│ _label.py          │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ Labeled Dataset    │
│ L{n}_{hash}.jpg    │
└────────────────────┘
```

### Phase 4: Validation and Analysis

```
┌────────────────┐
│  Mapping CSV   │
└────────┬───────┘
         │
         ├─────────────┬──────────────┐
         ▼             ▼              ▼
┌──────────────┐ ┌──────────┐ ┌───────────┐
│ Accuracy     │ │ Plots    │ │ Stats     │
│ Check        │ │ Scripts  │ │ Analysis  │
└──────────────┘ └──────────┘ └───────────┘
```



## Dependencies

### requirement.txt

```txt
Pillow>=10.0.0           # Image manipulation
imagehash>=4.3.1         # Perceptual hashing
pandas>=2.0.0            # CSV data management
tqdm>=4.65.0             # Progress bars
scikit-image>=0.21.0     # SSIM and image metrics
numpy>=1.24.0            # Array operations
```

### Installation

```bash
pip install -r requirement.txt
```

### Python Versions

- **Minimum:** Python 3.8+
- **Recommended:** Python 3.10+


## Results and Output

### Quality Metrics

**Based on current results:**

#### Hamming Distance
- **Typical range:** 0-50 for correct matches
- **Warning threshold:** > 120
- **Dataset mean:** ~8.34

#### SSIM (Structural Similarity)
- **Range:** 0.0 - 1.0
- **Excellent:** > 0.95
- **Good:** 0.85 - 0.95
- **Acceptable:** 0.70 - 0.85
- **Problematic:** < 0.70
- **Dataset mean:** ~0.978

#### Matching Accuracy
- **Excellent matches (SSIM > 0.95):** ~95.83%
- **Total matches:** ~12,000
- **False positives:** < 1%

### Main Output Files

1. **Hash CSVs:**
   - `jpeg_hashes_all_labels.csv` (~12,000 rows)
   - Hash for each JPEG image

2. **Mapping CSVs:**
   - Per category: `{Label}_all_tiff_to_jpeg_mapping.csv`
   - Total: `n_tiff.csv` (1, 100, 1000 TIFFs)

3. **Plots:**
   - `hamming_histogram_logscale.png`
   - `ssim_histogram.png`
   - `ssim_plot_by_row.png`

4. **Reports:**
   - `compare_accuracy_results.txt`

### Final Dataset

**Organization:**
```
public_dataset/
├── Complete_dataset/
│   ├── Biological/
│   │   ├── L0_00ba59bffe72a8b6a61ebae80fcfcf1d.jpg
│   │   └── ...
│   ├── Fibres/
│   │   ├── L1_001ddb0f89bad9ae0f07dc1fa28f89f0.jpg
│   │   └── ...
│   └── [other categories]/
└── metadata/
    ├── mappings/
    ├── statistics/
    └── documentation/
```


## Technical Notes

### Perceptual Hash (pHash)

**Characteristics:**
- **Size:** 32×32 = 1024 bits
- **Robustness:** Invariant to:
  - Resizing
  - Light JPEG compression
  - Minor brightness/contrast changes
- **Sensitivity:** Detects structural changes

### SSIM (Structural Similarity Index)

**Formula:**
```
SSIM(x,y) = [l(x,y)]^α · [c(x,y)]^β · [s(x,y)]^γ
```
Where:
- l(x,y) = luminance comparison
- c(x,y) = contrast comparison  
- s(x,y) = structure comparison

**Advantages:**
- Correlated with human perception
- More accurate than MSE/PSNR
- Intuitive 0-1 range

### Image Standardization

**Pipeline:**
```python
1. Convert to grayscale (L mode)
2. Histogram equalization
3. Auto-contrast adjustment
4. Resize if needed (preserving aspect ratio)
```

**Motivation:**
- Uniformity in comparison
- Reduction of illumination variability
- Better algorithm performance



## Best Practices

### To Add New Images

1. **Place TIFFs in backup_folder/** under appropriate researcher
2. **Run conversion:**
   ```bash
   python scripts/jpeg_converter.py
   ```
3. **Generate hashes:**
   ```bash
   python scripts/hashing/create_jpeg_hashes_all_labels.py
   ```
4. **Run matching:**
   ```bash
   python scripts/comparing/compare.py
   ```
5. **Validate accuracy:**
   ```bash
   python scripts/metadata/general_accuracy.py
   ```

### For Custom Analysis

1. Use existing CSVs as base
2. Scripts in `sample_100/` for prototyping
3. Copy and modify scripts from `comparing/` or `metadata/`

### Performance Tips

- **Batch processing:** Use `optimized_*` versions of scripts
- **Memory:** Process categories separately for large datasets
- **I/O:** SSD recommended for optimal performance
- **CPU:** Scripts benefit from multi-threading (4+ cores)


## Troubleshooting

### Error: "Cannot open TIFF file"

**Cause:** Corrupted TIFF file or unsupported format

**Solution:**
```bash
# Verify integrity
identify -verbose file.tif
# Convert with ImageMagick if necessary
convert file.tif -quality 100 file.jpg
```

### Error: "Out of memory"

**Cause:** Too many files processed simultaneously

**Solution:**
- Process by category
- Reduce batch size in scripts
- Use `gc.collect()` periodically

### Unexpectedly low SSIM

**Possible causes:**
1. Different images (incorrect match)
2. Unhandled different resolution
3. Corruption during conversion

**Debug:**
```python
# Visualize images
from PIL import Image
import matplotlib.pyplot as plt

img1 = Image.open("tiff_path")
img2 = Image.open("jpeg_path")
plt.subplot(121); plt.imshow(img1)
plt.subplot(122); plt.imshow(img2)
plt.show()
```


## Contacts and References

### Scientific Documentation

See `sem_dataset_paper.pdf` for details on:
- Image acquisition methodology
- SEM technical specifications
- Experimental protocols
- Related publications


## Changelog

### Current Version
- Dataset: ~12,000 labeled JPEG images
- 10 scientific categories
- Matching accuracy: >95%
- Complete scripts for end-to-end pipeline


## License and Usage

**Note:** Check with project manager for information on:
- Dataset license
- Usage restrictions
- Required citations
- Publication policies



**Last updated:** December 2025  
**Documentation version:** 1.0 
