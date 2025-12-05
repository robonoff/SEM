# SEM Dataset Project

A comprehensive pipeline for processing, analyzing, and organizing Scanning Electron Microscopy (SEM) images. This project handles TIFF to JPEG conversion, perceptual hashing, image matching, and automated labeling of ~38,000 microscopy images across 10 scientific categories.

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Dataset Description](#dataset-description)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
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
├── scripts/                    # Processing scripts (see scripts/README.md)
│   ├── jpeg_converter.py       # TIFF → JPEG conversion
│   ├── comparing/              # Image matching scripts
│   ├── hashing/                # Hash generation scripts
│   ├── labeling/               # Image labeling scripts
│   ├── metadata/               # Accuracy analysis scripts
│   ├── plots/                  # Visualization scripts
│   └── csv/                    # Data files and mappings
│       └── n_tiff_to_all_jpeg_mapping/  # TIFF-JPEG mapping results
├── requirement.txt             # Python dependencies
├── sem_dataset_paper.pdf       # Scientific documentation
└── output.txt                  # Complete folder structure reference
```

> **Note**: CSV data files are not included in the repository. They will be generated when you run the scripts.

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

- **Total Images**: ~38,000 TIFF files
- **Source Directories**: 981 researcher folders
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

### 1. Convert TIFF to JPEG

```bash
cd scripts
python jpeg_converter.py
# Enter input folder path (where your TIFF files are)
# Enter output folder path (where to save JPEG files)
```

### 2. Generate Image Hashes

```bash
cd scripts/hashing
python create_jpeg_hashes_all_labels.py
```

This creates a CSV file with perceptual hashes for all JPEG images.

### 3. Match JPEG to TIFF

```bash
cd scripts/comparing
python compare.py
```

This matches converted JPEGs to their original TIFF files using Hamming distance and SSIM.

### 4. Assign Labels

```bash
cd scripts/labeling
python copy_and_assign_label.py
```

This copies and renames images with category labels (L0-L9).

### 5. Validate Results

```bash
cd scripts/metadata
python general_accuracy.py
```

This generates accuracy reports and statistics.

### 6. Visualize Results

```bash
cd scripts/plots
python hamming_histogram.py
python ssim_histogram.py
```

This creates histograms showing match quality distribution.

## Documentation

### Detailed Documentation

- **[Scripts Documentation](scripts/README.md)**: Comprehensive guide to all scripts, their functions, and usage
- **Scientific Paper**: See `sem_dataset_paper.pdf` for methodology and research context
- **Complete Structure**: See `output.txt` for full directory tree

### Processing Pipeline

```
┌─────────────────────┐
│  1. TIFF Files      │
│  (Original Data)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. JPEG Conversion │
│  (jpeg_converter)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. Hash Generation │
│  (create_hashes)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. Image Matching  │
│  (compare.py)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  5. Label Assignment│
│  (assign_label)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  6. Validation      │
│  (accuracy check)   │
└─────────────────────┘
```

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

## Project Status

### Completed Features

- ✅ TIFF to JPEG conversion with quality preservation
- ✅ Perceptual hash generation with image standardization
- ✅ Dual-metric matching (Hamming + SSIM)
- ✅ Automated category labeling (10 classes)
- ✅ Comprehensive accuracy validation
- ✅ Visualization tools for quality assessment

### Repository Notes

- CSV data files are excluded from version control (see `.gitignore`)
- Generated data will be stored in `scripts/csv/` when you run the scripts
- Large binary files (TIFF/JPEG images) are not included in this repository

## Performance Tips

- **Batch Processing**: Use optimized versions for >1000 images
- **Memory Management**: Process categories separately for large datasets
- **Storage**: SSD recommended for I/O intensive operations
- **CPU**: Multi-threading benefits from 4+ cores

## Contributing

When contributing to this project:

1. Follow the existing code structure and naming conventions
2. Update documentation for new features
3. Test with sample datasets before processing full data
4. Include docstrings and comments for complex algorithms
5. Update `requirement.txt` if adding new dependencies

## Troubleshooting

### Common Issues

**"File not found" errors**: 
- Update absolute paths in script headers to match your environment

**"Out of memory" errors**:
- Process data by category instead of all at once
- Use sample scripts for testing before full runs

**Low SSIM values**:
- Verify images are properly standardized
- Check for resolution mismatches
- Use visualization scripts to identify problematic matches

For more detailed troubleshooting, see [scripts/README.md](scripts/README.md).

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
**Maintainer**: Roberta Lamberti
