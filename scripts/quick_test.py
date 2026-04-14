"""Quick Test Script for SlicerSegmentationDemo

Run this script in the 3D Slicer Python console (View > Python Console)
to verify the module works correctly without using the UI.

Usage:
    1. Open 3D Slicer
    2. Open the Python console (View > Python Console)
    3. Copy and paste this entire script into the console
    4. Press Enter to execute

Expected output:
    - MRHead volume loads and appears in slice views
    - Segmentation overlay appears after processing
    - Console prints confirmation messages
"""

import SampleData
import slicer
import SimpleITK as sitk
import sitkUtils

# --- Step 1: Load MRHead sample data ---
print("[1/4] Loading MRHead sample data...")
volume_node = SampleData.downloadSample("MRHead")
assert volume_node is not None, "Failed to load MRHead"
print(f"      Loaded: {volume_node.GetName()}")
print(f"      Dimensions: {volume_node.GetImageData().GetDimensions()}")

# --- Step 2: Pull into SimpleITK and apply smoothing ---
print("[2/4] Applying Gaussian smoothing (sigma=1.0)...")
sitk_image = sitkUtils.PullVolumeFromSlicer(volume_node)
smoothed = sitk.SmoothingRecursiveGaussian(sitk_image, 1.0)
print("      Smoothing complete.")

# --- Step 3: Apply threshold segmentation ---
print("[3/4] Applying threshold segmentation [100, 3000]...")
segmented = sitk.BinaryThreshold(
    smoothed,
    lowerThreshold=100,
    upperThreshold=3000,
    insideValue=1,
    outsideValue=0,
)
print("      Thresholding complete.")

# --- Step 4: Push result back to Slicer ---
print("[4/4] Creating label map in Slicer scene...")
label_node = sitkUtils.PushVolumeToSlicer(segmented, None, "QuickTestSegmentation", "LabelMap")
slicer.util.setSliceViewerLayers(background=volume_node, label=label_node)
slicer.util.resetSliceViews()

assert label_node is not None, "Failed to create label map"
print("")
print("Quick test PASSED.")
print(f"Output node: {label_node.GetName()}")
print("Check the slice views for the segmentation overlay.")
