# SEM Dataset Project

A comprehensive pipeline for processing, analyzing, and organizing Scanning Electron Microscopy (SEM) images. This project handles TIFF to JPEG conversion, perceptual hashing, image matching, and automated labeling of microscopy images across 10 scientific categories.

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Dataset Description](#dataset-description)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [License](#license)

## Project Overview

This repository provides tools for:

- **TIFF to JPEG Conversion**: High-quality batch conversion (100% quality)
- **Perceptual Hashing**: Generate pHash for image similarity matching
- **Image Matching**: Match converted JPEGs to original TIFFs using Hamming distance and SSIM
- **Automated Labeling**: Organize images by scientific categories with standardized naming
- **Quality Validation**: Accuracy metrics and visualization tools

### Key Features

- **Large-scale processing**: Handles 38,000+ images efficiently
- **High accuracy**: >95% matching accuracy with SSIM validation
- **Modular design**: Independent scripts for each processing step
- **Comprehensive metrics**: Hamming distance, SSIM, and statistical analysis
- **Visualization**: Histograms and plots for quality assessment

## Repository Structure

```
SEM/
├── LICENSES/                   # License files (MIT)
├── scripts/                    # Processing scripts
│   ├── jpeg_converter.py       # TIFF → JPEG conversion script
│   ├── comparing/              # Image matching algorithms
│   │   ├── compare_n_tiff_to_jpeg.py
│   │   └── optimized_compare_n_tiff_to_all_jpeg.py
│   ├── hashing/                # Perceptual hash generation
│   │   ├── create_jpeg_hashes_all_labels.py
│   │   └── create_jpeg_hashes_single_label.py
│   ├── labeling/               # Image labeling and organization
│   │   └── copy_.and_assign_true_labels.py
│   ├── metadata/               # Accuracy validation
│   │   └── compare_accuracy_results.txt
│   └── csv/                    # Generated data files
│       └── n_tiff_to_all_jpeg_mapping/
├── requirement.txt             # Python dependencies
├── sem_dataset_paper.pdf       # Scientific paper and methodology
└── output.txt                  # Complete original dataset structure
```

### Folder Contents

#### `scripts/`
Main processing pipeline for the SEM dataset:

- **`jpeg_converter.py`**: Standalone script that converts TIFF images to JPEG format (100% quality)
- **`comparing/`**: Scripts that match converted JPEGs to original TIFFs using perceptual hashing and SSIM
- **`hashing/`**: Scripts that generate perceptual hashes (pHash) for images to enable similarity matching
- **`labeling/`**: Scripts that organize and rename images with category labels (L0-L9)
- **`metadata/`**: Accuracy analysis results and validation metrics
- **`csv/`**: Generated CSV files with image mappings and hash values (most excluded from repo)

#### Root Files

- **`LICENSES/`**: MIT license text for REUSE compliance
- **`requirement.txt`**: Python package dependencies for all scripts
- **`sem_dataset_paper.pdf`**: Research paper with detailed methodology


## Dataset Description

### Categories

The dataset consists of **10 scientific categories** of SEM images:

| Label | Category | Description |
|-------|----------|-------------|
| L0 | Biological | Biological samples and organisms |
| L1 | Fibres | Fibers and fibrous structures |
| L2 | Films_Coated_Surface | Films and coated surfaces |
| L3 | MEMS_devices_and_electrodes | MEMS devices and electrodes |
| L4 | Nanowires | Nanowire structures |
| L5 | Particles | Nanoparticles and microparticles |
| L6 | Patterned_surface | Patterned and structured surfaces |
| L7 | Porous_Sponge | Porous materials and sponges |
| L8 | Powder | Powder samples |
| L9 | Tips | Microscopy tips and probes |

### Dataset Statistics

- **Total Images**: 10 jpeg compressed files
- **Total tiff Images to match in order labelled:** 25518 tiff files
- **Source Directories**: [NFFA-EUROPE - Majority SEM Dataset](https://b2share.eudat.eu/records/e344a8afef08463a855ada08aadbf352)
- **Format**: Original TIFF (lossless), Converted JPEG (100% quality)
- **Organization**: By researcher and experiment date

### File Naming Convention

Labeled JPEG files follow this format:
```
L{category_number}_{perceptual_hash}.jpg
```

Example: `L5_001eb7a9c7c13bda29f79ee18c84a43e.jpg` (Particles category)

## Installation

### Prerequisites

- Python 3.8 or higher (Python 3.10+ recommended)
- pip package manager

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/robonoff/SEM.git
cd SEM
```

2. **Install dependencies**:
```bash
pip install -r requirement.txt
```

### Dependencies

The project requires the following Python packages:

```
Pillow>=10.0.0           # Image processing
imagehash>=4.3.1         # Perceptual hashing
pandas>=2.0.0            # Data management
tqdm>=4.65.0             # Progress bars
scikit-image>=0.21.0     # SSIM metrics
numpy>=1.24.0            # Numerical operations
matplotlib>=3.7.0        # Visualization
```

## Quick Start

### 1. Generate Image Hashes

```bash
cd scripts/hashing
python create_jpeg_hashes_all_labels.py
```

This creates a CSV file with perceptual hashes for all JPEG images.

### 2. Match JPEG to TIFF

```bash
cd scripts/comparing
python compare.py
```

This matches converted JPEGs to their original TIFF files using Hamming distance and SSIM.

### 3. Assign Labels to TIFF

```bash
cd scripts/labeling
python copy_and_assign_label.py
```

This copies and renames images with category labels (L0-L9).

## Key Algorithms

### Perceptual Hashing (pHash)

- **Hash Size**: 32×32 (1024 bits)
- **Algorithm**: Discrete Cosine Transform (DCT) based
- **Preprocessing**: Grayscale conversion, histogram equalization, auto-contrast
- **Purpose**: Robust image fingerprinting for similarity matching

### Image Matching

1. **Hamming Distance**: Fast initial comparison between hashes
   - Threshold: < 150 for preliminary matching
   - Threshold: < 120 for triggering SSIM

2. **SSIM (Structural Similarity Index)**: Precise similarity measurement
   - Range: 0.0 (completely different) to 1.0 (identical)
   - Threshold: > 0.95 for "excellent" matches
   - Average: ~0.978 across dataset

### Quality Metrics

- **Match Accuracy**: >95.83% excellent matches (SSIM > 0.95)
- **Mean SSIM**: 0.978
- **Mean Hamming Distance**: 8.34

## Performance Tips

- **Batch Processing**: Use optimized versions for >1000 images
- **Memory Management**: Process categories separately for large datasets
- **Storage**: SSD recommended for I/O intensive operations

## Contributing

When contributing to this project:

1. Follow the existing code structure and naming conventions
2. Update documentation for new features
3. Test with sample datasets before processing full data
4. Include docstrings and comments for complex algorithms
5. Update `requirement.txt` if adding new dependencies

## License

This project is licensed under the MIT License. See individual files for copyright information.

## Citation

If you use this dataset or code in your research, please cite:

```
[Citation information from sem_dataset_paper.pdf]
```

## Contact

For questions or issues:
- Open an issue on GitHub
- See `sem_dataset_paper.pdf` for research contacts

---

**Last Updated**: December 2025  
**Repository**: https://github.com/robonoff/SEM  
**Maintainer**: Jacopo Zuppa, Riccardo Simonetti, Sandeep Chavuladi, Roberta Lamberti