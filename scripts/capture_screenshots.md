# Screenshot Capture Helper Guide

This guide provides step-by-step instructions for capturing publication-quality screenshots of SlicerSegmentationDemo.

## Prerequisites

- **3D Slicer 5.0+** installed and running
- **SlicerSegmentationDemo module** path configured in Slicer settings
- **Screenshot tool**: Built-in OS tool OR one of:
  - macOS: Gifox or LICEcap for GIF recording
  - Windows: ScreenToGif
  - Linux: SimpleScreenRecorder

## Workflow

### Step 1: Prepare Slicer Environment
```
1. Open 3D Slicer
2. Go to Modules > Examples > SlicerSegmentationDemo
3. Set Layout: View > Layout > Four-Up
4. Resize window: ~1400 x 900 pixels
5. Clear any previous data: File > New Scene
```

**Result**: Clean Slicer window with module panel visible on left

---

### Step 2: Capture `main-workflow.png`

**Timeline**: ~30 seconds

```
1. In module panel, click "Load MRHead Sample Data"
   ⏱ Wait: 3-5 seconds for download/load
   
2. Observe MRHead data appears in all 4 views
   ⏱ Wait: 2 seconds to stabilize rendering
   
3. Take screenshot:
   - macOS: Cmd+Shift+4 > drag to select window
   - Windows: Snip & Sketch or Print Screen
   - Slicer: Edit > Take Screenshot
   
4. Save as: screenshots/main-workflow.png
   Format: PNG
   Size: ~400-500 KB
```

**Verification Checklist**:
- [ ] Module panel fully visible on left side
- [ ] All parameter sliders visible
- [ ] Four slice views show MRHead volume (grayscale)
- [ ] Status label shows "MRHead loaded successfully"
- [ ] Image is sharp and well-lit

---

### Step 3: Capture `segmentation-view.png`

**Timeline**: ~20 seconds

```
1. (Continuing from Step 2 state)
   Segmentation parameters should be visible:
   - Smoothing Sigma: 1.0 (default)
   - Lower Threshold: 100 (default)
   - Upper Threshold: 3000 (default)
   - Morphological Closing: ✓ (checked/enabled)
   
2. Click "Apply Segmentation" button
   ⏱ Wait: 2-3 seconds for processing
   
3. Status updates to: "Segmentation complete"
   ⏱ Wait: 1 second for rendering
   
4. Navigate to clear slice:
   - Scroll middle mouse wheel through slices OR
   - Adjust "Slice Offset" sliders on each view
   - Goal: Find axial slices showing segmented brain tissue clearly
   - Typically around 60-70% through the volume
   
5. Take screenshot:
   - Option A: Full Slicer window (includes module panel)
   - Option B: Crop to slice views only (4-panel view)
   Recommend Option A for context
   
6. Save as: screenshots/segmentation-view.png
   Format: PNG
   Size: ~400-500 KB
```

**Verification Checklist**:
- [ ] Brain tissue regions are clearly segmented (colored overlay)
- [ ] Overlay color is distinct and visible (not the same as background)
- [ ] Multiple slice views show consistent segmentation
- [ ] No errors or artifacts visible
- [ ] Image clearly shows before (MRHead) and after (segmentation) comparison

---

### Step 4: Capture `demo.gif` (Optional but Recommended)

**Timeline**: ~1-2 minutes to record + process

```
A. START RECORDING
   - Open screen recorder (Gifox, LICEcap, or built-in tool)
   - Set region: Full Slicer window (~1400 x 900)
   - Set FPS: 10-15 fps (smooth but smaller file size)
   - Click "Record" or start capturing
   
B. PERFORM WORKFLOW (Speak through steps if possible)
   
   [00:00-01:00] Module Selection & View
   - Click on Modules dropdown at top of Slicer
   - Select Examples > SlicerSegmentationDemo
   - Status shows "Ready"
   - Hold and observe for 1 second
   
   [01:00-06:00] Load Data
   - Click "Load MRHead Sample Data" button
   - Watch the module panel and slice views
   - Slicing appears in four views as download completes (~3 sec)
   - Hold to observe loaded MRHead
   
   [06:00-08:00] Parameter Review
   - Pause and highlight the parameter sliders
   - Show: Sigma slider, threshold sliders
   - Hover over parameters to show tooltips
   
   [08:00-12:00] Run Segmentation
   - Click "Apply Segmentation" button
   - Watch status update to "Running segmentation..."
   - Observe processing (momentary compute time)
   - Status updates to "Segmentation complete"
   
   [12:00-18:00] View Results
   - Scroll through axial, sagittal, and coronal slices
   - Show segmentation overlay on multiple slices
   - Highlight the color-coded brain tissue regions
   
   [18:00-20:00] Wrap-up
   - Return to center view
   - Let rendering settle
   - End recording
   
   TOTAL: ~20 seconds of screen recording

C. CONVERT TO GIF
   If recorded as .mov or .mp4:
   
   macOS/Linux:
   ffmpeg -i recording.mov \
     -vf "fps=10,scale=900:-1" \
     -loop 0 \
     -c:v gif \
     demo.gif
   
   Windows (with ffmpeg installed):
   ffmpeg -i recording.mp4 -vf "fps=10,scale=900:-1" ^
     -loop 0 demo.gif

D. OPTIMIZE IF NEEDED
   If demo.gif > 5 MB:
   
   ffmpeg -i demo.gif \
     -vf "fps=8,scale=700:-1" \
     -loop 0 \
     demo_optimized.gif
   
E. Save as: screenshots/demo.gif
   Target size: < 5 MB
   Duration: 15-20 seconds
```

**Verification Checklist**:
- [ ] Full workflow visible (module selection through segmentation result)
- [ ] Each step is clear and distinguishable
- [ ] GIF loops smoothly with no glitches
- [ ] File size < 5 MB (GitHub friendly)
- [ ] Playback is legible (not too fast, not too slow)

---

## Post-Capture Steps

1. **Move images to repo**:
   ```bash
   mv main-workflow.png /path/to/SlicerSegmentationDemo/screenshots/
   mv segmentation-view.png /path/to/SlicerSegmentationDemo/screenshots/
   mv demo.gif /path/to/SlicerSegmentationDemo/screenshots/
   ```

2. **Verify files in git**:
   ```bash
   cd /path/to/SlicerSegmentationDemo
   git add screenshots/
   git status
   ```

3. **Update README references** (if not already done):
   - Verify [README.md](../README.md) references the images
   - Test links on GitHub

4. **Commit**:
   ```bash
   git commit -m "Add real screenshots of module UI and segmentation results"
   git push
   ```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module doesn't appear in dropdown | Restart Slicer or check module path configuration |
| Data download fails | Check internet connection; MRHead is ~30 MB |
| Segmentation takes too long | Normal processing is 1-2 seconds; check system resources |
| Screenshot colors look wrong | Use PNG format, ensure 24-bit or 32-bit color mode |
| GIF is too large (> 5 MB) | Reduce frame rate (fps=8) or resolution in ffmpeg command |
| GIF playback stutters | Reduce FPS to 8 or 10 fps |

---

## Tips for Professional Results

1. **Lighting**: Keep Slicer on plain background (close other windows)
2. **Timing**: Speak through steps slowly; viewers should understand what's happening
3. **Quality**: PNG format for images, GIF for animation (both lossless at final stage)
4. **Consistency**: Use same window size and layout for all captures
5. **Validation**: Open final images in browser/GitHub preview to verify quality

---

## Example Commands

Save entire workflow as script:

```bash
# Capture main workflow
screencapture -x -w main-workflow.png

# Capture segmentation view (macOS)
screencapture -x -s segmentation-view.png

# Create GIF from mov (macOS with ffmpeg)
ffmpeg -i demo.mov -vf "fps=10,scale=900:-1" -c:v gif demo.gif

# Add to git
git add screenshots/*.png screenshots/*.gif
git commit -m "Add screenshot captures"
git push
```

---

For questions or issues, refer to [screenshots/README.md](README.md) for detailed capture instructions.
