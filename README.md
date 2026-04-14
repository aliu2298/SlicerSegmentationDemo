# SlicerSegmentationDemo

**Automated Brain Tissue Segmentation Module for 3D Slicer**

[![Slicer](https://img.shields.io/badge/3D%20Slicer-Module-blue)](https://www.slicer.org/) [![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

SlicerSegmentationDemo is a Python scripted module for [3D Slicer](https://www.slicer.org/) that automates a basic brain tissue segmentation workflow. It loads the built-in **MRHead** sample dataset, applies Gaussian smoothing for noise reduction, and generates a threshold-based segmentation of brain tissue—all through a clean module UI panel. This project is designed as a self-contained work sample demonstrating familiarity with the Slicer platform, Python scripted modules, and reproducible medical imaging workflows.

## Why This Project

Medical image segmentation is a core task in clinical research and surgical planning. This module demonstrates:

- Practical use of Slicer’s Python scripted module framework
- Working with volumetric MRI data programmatically
- Automated segmentation using threshold-based approaches
- Clean documentation and reproducible setup using only built-in sample data

No private datasets or external dependencies are required. Any reviewer can clone this repo and run the full workflow in under 5 minutes.

## Demo

Real screenshots from running the module in 3D Slicer:

| View | Description |
|------|-------------|
| ![Main Workflow](screenshots/main-workflow.png) | Module panel loaded in Slicer with MRHead data |
| ![Segmentation View](screenshots/segmentation-view.png) | Brain tissue segmentation overlay on MRI slices |
| ![Demo GIF](screenshots/demo.gif) | Full workflow from load to segmentation in ~30 seconds |

**Note**: Screenshots are placeholders. To capture real images, follow the [screenshot capture guide](screenshots/README.md) or [detailed instructions](scripts/capture_screenshots.md).

## Features

- **One-click sample data loading** — uses Slicer’s built-in MRHead dataset
- **Gaussian smoothing** — configurable sigma for noise reduction
- **Threshold segmentation** — adjustable lower/upper bounds for brain tissue isolation
- **Clean module UI** — parameter controls with Apply button in the standard Slicer module panel
- **Visible output** — segmentation node displayed as a colored overlay in slice views
- **No external dependencies** — runs entirely within a standard 3D Slicer installation

## Tech Stack

| Component | Details |
|-----------|---------|
| Platform | [3D Slicer](https://www.slicer.org/) 5.x |
| Language | Python 3.9+ (Slicer embedded) |
| Libraries | `slicer`, `vtk`, `SimpleITK`, `SampleData` (all bundled with Slicer) |
| Module type | Scripted module (no C++ required) |

## Installation

### Option 1: Load as a local module (recommended for review)

1. **Download** [3D Slicer](https://download.slicer.org/) (version 5.0 or later)
2. **Clone** this repository:
   ```bash
   git clone https://github.com/aliu2298/SlicerSegmentationDemo.git
   ```
3. **Add the module path** in Slicer:
   - Open Slicer → `Edit` → `Application Settings` → `Modules`
   - Under *Additional module paths*, click `Add` and browse to:
     ```
     /path/to/SlicerSegmentationDemo/module
     ```
   - Click `OK` and restart Slicer when prompted
4. The module will appear under **Examples → SlicerSegmentationDemo** in the module dropdown

### Option 2: Future extension packaging

This module could be packaged as a Slicer extension for distribution through the Slicer Extensions Manager. See the [Slicer extension development guide](https://slicer.readthedocs.io/en/latest/developer_guide/extensions.html) for details.

## How to Run

1. Open 3D Slicer with the module path configured (see Installation above)
2. Navigate to **Examples → SlicerSegmentationDemo** in the module selector
3. Click **Load MRHead Sample Data** to load the built-in MRI volume
4. Adjust parameters if desired:
   - **Smoothing Sigma**: controls Gaussian blur strength (default: 1.0)
   - **Lower Threshold**: minimum intensity for segmentation (default: 100)
   - **Upper Threshold**: maximum intensity for segmentation (default: 3000)
5. Click **Apply Segmentation** to run the workflow
6. The segmentation overlay appears on all three slice views

## Sample Workflow

```
Open Slicer → Select SlicerSegmentationDemo module
     ↓
Click "Load MRHead Sample Data"
     ↓
MRHead volume appears in slice views
     ↓
Adjust smoothing sigma and threshold values (optional)
     ↓
Click "Apply Segmentation"
     ↓
Brain tissue segmentation overlay is displayed
     ↓
Inspect results in Axial, Sagittal, and Coronal views
```

## Repository Structure

```
SlicerSegmentationDemo/
├── README.md                              # This file
├── LICENSE                                # MIT License
├── .gitignore                             # Python gitignore
├── screenshots/
│   ├── README.md                          # Screenshot capture instructions
│   ├── main-workflow.png                  # (placeholder) Module panel in Slicer
│   ├── segmentation-view.png              # (placeholder) Segmentation result
│   └── demo.gif                           # (placeholder) Full workflow recording
├── docs/
│   ├── workflow.md                        # Step-by-step user workflow
│   └── architecture.md                    # Module architecture explanation
├── module/
│   └── SlicerSegmentationDemo.py          # Main scripted module
├── scripts/
│   └── quick_test.py                      # Quick validation script for Slicer Python console
└── sample-output/
    └── results.md                         # Expected output description
```

## Limitations

- **Threshold-based segmentation only** — this is a demonstration, not a production-grade tool. Real clinical workflows use more advanced methods (atlas-based, deep learning, etc.)
- **Single dataset** — tested with MRHead only; behavior on other volumes may vary
- **No 3D surface export** — the current version produces a label map overlay but does not export STL/OBJ models
- **No automated testing** — validation is manual through the quick_test script
- **UI is minimal** — focuses on demonstrating the module pattern rather than full-featured controls

## Future Improvements

- [ ] Add 3D model export (STL) from segmentation results
- [ ] Implement region growing or watershed segmentation as an alternative method
- [ ] Add automated unit tests using Slicer’s testing framework
- [ ] Package as a proper Slicer extension with CMakeLists.txt and extension metadata
- [ ] Add support for additional sample datasets (CT Chest, MRBrainTumor)
- [ ] Include before/after comparison view in the module UI

## About / Submission Note

This repository was created as a **work sample** to demonstrate familiarity with 3D Slicer development, Python scripted modules, and medical imaging workflows. It is intentionally scoped to be small, reproducible, and easy to review.

The code follows the standard Slicer scripted module pattern (Widget, Logic, and Test classes) and uses only built-in sample data and bundled libraries. Slicer’s own scripted modules (accessible via the module list) served as reference examples for the module structure.

**Author**: Oluwarotimi Aliu  
**Contact**: [GitHub Profile](https://github.com/aliu2298)

---

## How to Turn This Repo into a Strong Portfolio Piece

1. **Capture real screenshots**: Run the module, take screenshots of the Slicer interface showing the module panel, slice views with data loaded, and the segmentation overlay. Replace the placeholder images in `screenshots/`.

2. **Record a demo GIF**: Use a screen recorder to capture the full workflow (load data → apply segmentation → inspect results). Keep it under 30 seconds. Tools: [LICEcap](https://www.cockos.com/licecap/), [Gifox](https://gifox.app/), or QuickTime + ffmpeg.

3. **Add actual result data**: After running the module, note the number of voxels segmented, volume measurements, or other quantitative output in `sample-output/results.md`.

4. **Pin the repo** on your GitHub profile so it appears at the top of your profile page.

5. **Add topics** to the repo: `3d-slicer`, `medical-imaging`, `segmentation` (Settings → Topics).

6. **Link in applications**: Reference this repo URL directly in job applications or cover letters with a one-line description of what it demonstrates.

7. **Extend the module**: Even one additional feature (like 3D model export or a second segmentation method) significantly strengthens the sample.
