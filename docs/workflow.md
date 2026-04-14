# Workflow Guide

Step-by-step instructions for running the SlicerSegmentationDemo module.

## Prerequisites

- 3D Slicer 5.0 or later installed
- Module path added in Slicer settings (see README for installation)

## Steps

### 1. Open 3D Slicer

Launch 3D Slicer from your Applications folder or Start menu.

### 2. Navigate to the Module

Use the module selector dropdown (top-left of the Slicer window):

**Examples > SlicerSegmentationDemo**

The module panel will appear on the left side of the Slicer interface.

### 3. Load Sample Data

Click the **"Load MRHead Sample Data"** button in the Sample Data section.

- Slicer will download the MRHead dataset (approximately 30 MB)
- The MRI volume will appear in all three slice views (Axial, Sagittal, Coronal)
- Status label will update to "MRHead loaded successfully"

### 4. Configure Parameters (Optional)

The default parameters work well for MRHead. You can adjust:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Smoothing Sigma | 1.0 | Gaussian blur strength in mm. Higher values = more smoothing. |
| Lower Threshold | 100 | Minimum voxel intensity to include in segmentation. |
| Upper Threshold | 3000 | Maximum voxel intensity to include in segmentation. |

### 5. Run Segmentation

Click **"Apply Segmentation"**.

- The module applies Gaussian smoothing to the volume
- A binary threshold creates a label map of brain tissue
- The segmentation overlay appears as a colored layer on all slice views
- Status label will update to "Segmentation complete"

### 6. Inspect Results

- Scroll through slices in each view to examine the segmentation
- Use the slice offset slider bars below each view
- Toggle the label map visibility in the slice view controls if needed

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not in dropdown | Verify the module path is correctly added in Edit > Application Settings > Modules, then restart Slicer |
| Data fails to load | Check internet connection; MRHead downloads from Slicer's data server |
| No segmentation visible | Ensure label map visibility is enabled in slice view controls |
| Poor segmentation result | Adjust threshold values; try lower=50, upper=2000 for a different result |
