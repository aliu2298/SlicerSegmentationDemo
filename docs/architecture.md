# Module Architecture

This document explains how the SlicerSegmentationDemo module is organized.

## Slicer Scripted Module Pattern

3D Slicer scripted modules follow a standard four-class pattern. This module implements all four classes in a single Python file (`module/SlicerSegmentationDemo.py`).

## Class Overview

```
SlicerSegmentationDemo.py
│
├── SlicerSegmentationDemo          (Module descriptor)
│   └── Metadata: title, category, contributors, help text
│
├── SlicerSegmentationDemoWidget     (UI / presentation)
│   ├── setup()          → Builds the module panel UI
│   ├── onLoadData()     → Handles "Load MRHead" button click
│   └── onApplySegmentation() → Handles "Apply" button click
│
├── SlicerSegmentationDemoLogic      (Processing / business logic)
│   └── runSegmentation() → Smoothing + threshold pipeline
│
└── SlicerSegmentationDemoTest       (Self-test)
    └── test_FullWorkflow() → End-to-end validation
```

## Class Details

### SlicerSegmentationDemo (Module Descriptor)

Registers the module with Slicer. Sets:
- **title**: Display name in the module selector
- **categories**: Where it appears in the module menu (`Examples`)
- **contributors**: Author attribution
- **helpText**: HTML help shown in the module panel

### SlicerSegmentationDemoWidget (UI)

Builds the module panel using Slicer/Qt widgets:
- **Sample Data section**: Button to load MRHead
- **Segmentation Parameters section**: Sliders for sigma, lower/upper threshold
- **Apply button**: Triggers the processing pipeline
- **Status label**: Shows current state to the user

The Widget delegates all processing to the Logic class, keeping UI and computation separate.

### SlicerSegmentationDemoLogic (Processing)

Contains the actual image processing pipeline:
1. Pulls the input volume into SimpleITK
2. Applies `SmoothingRecursiveGaussian` for noise reduction
3. Applies `BinaryThreshold` to isolate brain tissue
4. Pushes the result back as a Slicer label map node
5. Sets the label map as the overlay in slice views

This separation means the logic can be called from the UI, from tests, or from the Slicer Python console independently.

### SlicerSegmentationDemoTest (Self-Test)

Runs a basic end-to-end test:
1. Clears the scene
2. Loads MRHead via SampleData
3. Runs segmentation with default parameters
4. Asserts that output nodes exist

## Key Libraries Used

| Library | Purpose |
|---------|---------|
| `slicer` | Core Slicer Python API for scene, nodes, UI |
| `SimpleITK` | Image processing (smoothing, thresholding) |
| `sitkUtils` | Bridge between Slicer volumes and SimpleITK images |
| `SampleData` | Built-in module for downloading sample datasets |
| `vtk` | Underlying visualization toolkit (used by Slicer internally) |

## Data Flow

```
SampleData.downloadSample("MRHead")
        │
        ▼
vtkMRMLScalarVolumeNode (in Slicer scene)
        │
        ▼  sitkUtils.PullVolumeFromSlicer()
SimpleITK Image
        │
        ▼  SmoothingRecursiveGaussian()
Smoothed SimpleITK Image
        │
        ▼  BinaryThreshold()
Binary SimpleITK Image
        │
        ▼  sitkUtils.PushVolumeToSlicer()
vtkMRMLLabelMapVolumeNode (displayed as overlay)
```
