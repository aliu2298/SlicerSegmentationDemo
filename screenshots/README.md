# Screenshots

This folder contains screenshots and demo recordings of the SlicerSegmentationDemo module.

## Capture Instructions

Follow these steps to capture professional-quality screenshots for the repository.

### 1. Setup Slicer
1. Open 3D Slicer 5.x
2. Load the SlicerSegmentationDemo module via module selector: **Examples > SlicerSegmentationDemo**
3. Set layout to **Four-Up** (View > Layout > Four-Up) for best clarity
4. Resize Slicer window to approximately **1400 x 900 pixels**

### 2. Capture: main-workflow.png
**Purpose**: Show module panel with MRHead loaded in slice views

**Steps**:
1. Click **"Load MRHead Sample Data"** in the module panel
2. Wait for the volume to appear in all four views
3. Ensure the module panel (left side) is fully visible with all parameter controls
4. Capture using:
   - **Slicer built-in**: Edit > Take Screenshot (saves to Desktop)
   - **macOS**: Cmd+Shift+4, then click-drag to select the Slicer window
   - **Windows**: Print Screen or Snip & Sketch
5. Save as `main-workflow.png` (PNG format recommended for lossless quality)

**What should be visible**:
- ✅ Full Slicer window with module panel on left
- ✅ "Input Volume" section expanded with Load button
- ✅ "Segmentation Parameters" section with sliders
- ✅ "Post-Processing" section with morphology options
- ✅ Apply button visible
- ✅ Four slice views (axial, sagittal, coronal, 3D) showing MRHead volume

### 3. Capture: segmentation-view.png
**Purpose**: Show segmentation overlay on MRI slices

**Steps**:
1. (Continuing from previous state with MRHead loaded)
2. Adjust parameters if desired (defaults work well): sigma=1.0, threshold=[100, 3000]
3. Keep "Morphological Closing" **enabled** (checked) for cleaner results
4. Click **"Apply Segmentation"** button
5. Wait for status to show "Segmentation complete"
6. Adjust slice viewing to show clear segmentation overlay:
   - Use middle mouse scroll to step through slices
   - Or manually adjust the slice offset sliders
   - Try to find a slice where brain tissue is clearly segmented (usually axial slices through the middle of the brain)
7. Capture the slice views showing the colored label map overlay
   - Either full Slicer window OR
   - Just the four slice views (crop to those panels for focused view)
8. Save as `segmentation-view.png`

**What should be visible**:
- ✅ Axial, Sagittal, Coronal slices with MRHead (grayscale)
- ✅ Segmentation overlay (colored label map) clearly visible on top
- ✅ Brain tissue regions highlighted in distinct color (typically yellow/orange/green)
- ✅ Clear contrast between segmented and non-segmented regions

### 4. Capture: demo.gif (Optional but recommended)
**Purpose**: Animated walkthrough of complete workflow

**Steps**:
1. Start with clean Slicer scene
2. **Record screen** starting as you select the SlicerSegmentationDemo module
3. **Perform the workflow** step-by-step (slightly slower than normal for clarity):
   - Select module (2 seconds)
   - Click "Load MRHead" (wait for load, ~5 seconds)
   - Observe data in views (2 seconds)
   - Click "Apply Segmentation" (wait for processing, ~3 seconds)
   - Scroll through one or two slices to show segmentation (3 seconds)
4. **Total time**: ~15-20 seconds
5. **Recording methods**:
   - **macOS**: 
     - Option A: QuickTime Player > File > New Screen Recording > Record > Save (mov) > Convert to GIF
     - Option B: [Gifox](https://gifox.app/) for direct GIF recording (recommended)
     - Option C: [LICEcap](https://www.cockos.com/licecap/)
   - **Windows**:
     - Option A: Built-in Screen Recorder > Convert using ffmpeg
     - Option B: [ScreenToGif](https://www.screentogif.com/)
   - **Linux**:
     - Option A: SimpleScreenRecorder > Export to GIF
     - Option B: `ffmpeg -f x11grab -r 10 -s 1280x720 -i :0.0 demo.gif`

6. **Convert to GIF** (if needed):
   ```bash
   # macOS/Linux with ffmpeg installed
   ffmpeg -i recording.mov -vf "fps=10,scale=800:-1" -loop 0 demo.gif
   ```

7. **Optimize GIF size** (if > 5 MB):
   ```bash
   # Reduce colors and resolution
   ffmpeg -i demo.gif -vf "fps=8,scale=700:-1" -loop 0 demo_optimized.gif
   ```

8. Save as `demo.gif` (keep under 5 MB for best GitHub rendering)

**What should be visible**:
- ✅ Full workflow from module selection to final segmentation
- ✅ Data loading and processing steps
- ✅ UI interactions clearly visible
- ✅ Results displayed in slice views

## Tips for Best Results

| Aspect | Recommendation |
|--------|-----------------|
| **Resolution** | Capture at 1400x900 or larger; 1280x720 minimum for GIF |
| **Clarity** | Use Slicer's default dark theme for good contrast in screenshots |
| **Cropping** | Keep module panel visible in main-workflow.png to show UI design |
| **Overlay Quality** | Ensure label map color is clearly distinct from background |
| **File Format** | PNG for static images (lossless), GIF for animation |
| **File Sizes** | PNG ~200-500 KB each; GIF < 5 MB for GitHub |
| **Background** | Keep Slicer on plain desktop (no other windows cluttering the view) |

## File Storage

Place final images in this directory (`screenshots/`):
- `main-workflow.png` - Module panel with loaded data
- `segmentation-view.png` - Slice views with segmentation overlay  
- `demo.gif` - Animated workflow (optional, but recommended for impact)

Once captured, update `../README.md` to point to these files for GitHub rendering.
