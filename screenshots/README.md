# Screenshots

This folder contains screenshots and demo recordings of the SlicerSegmentationDemo module.

## Required Screenshots

After running the module in 3D Slicer, capture the following:

### main-workflow.png
**What to capture**: The full Slicer window showing the SlicerSegmentationDemo module panel on the left, with MRHead data loaded in the slice views.

**How**: Load MRHead via the module, then use `Edit > Take Screenshot` or your OS screenshot tool.

### segmentation-view.png
**What to capture**: The slice views (Axial, Sagittal, Coronal) with the segmentation overlay visible on top of the MRHead volume.

**How**: Run the segmentation, then capture the slice views showing the colored label map overlay.

### demo.gif
**What to capture**: An animated GIF showing the full workflow from opening the module to seeing the segmentation result.

**How**: Use a screen recording tool, then convert to GIF:
- macOS: QuickTime Player > File > New Screen Recording, then convert with `ffmpeg -i recording.mov -vf "fps=10,scale=800:-1" demo.gif`
- Or use [LICEcap](https://www.cockos.com/licecap/) or [Gifox](https://gifox.app/) to record directly as GIF
- Keep the GIF under 30 seconds and 5 MB for best GitHub rendering

## Tips

- Use Slicer's built-in screenshot tool (`Edit > Take Screenshot`) for clean captures
- Set the Slicer window to a reasonable size (1280x800 or similar) before capturing
- Ensure the module panel is visible and not collapsed
- Use the conventional layout (Four-Up or default) for the clearest view
