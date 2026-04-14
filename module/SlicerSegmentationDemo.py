"""SlicerSegmentationDemo - Automated Brain Tissue Segmentation Module

This is a 3D Slicer scripted module that demonstrates a basic brain tissue
segmentation workflow using the built-in MRHead sample dataset.

Module structure follows the standard Slicer scripted module pattern:
- SlicerSegmentationDemo: Module descriptor (metadata, icon, help text)
- SlicerSegmentationDemoWidget: UI panel with parameter controls
- SlicerSegmentationDemoLogic: Processing logic (smoothing + thresholding)
- SlicerSegmentationDemoTest: Basic self-test for validation
"""

import logging
import slicer
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleWidget,
    ScriptedLoadableModuleLogic,
    ScriptedLoadableModuleTest,
)
from slicer.util import VTKObservationMixin


# ---------------------------------------------------------------------------
# Module descriptor
# ---------------------------------------------------------------------------
class SlicerSegmentationDemo(ScriptedLoadableModule):
    """Metadata and help text shown in the Slicer module panel."""

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "SlicerSegmentationDemo"
        self.parent.categories = ["Examples"]
        self.parent.dependencies = []
        self.parent.contributors = ["Oluwarotimi Aliu"]
        self.parent.helpText = (
            "Automated brain tissue segmentation using MRHead sample data. "
            "Loads sample volume, applies Gaussian smoothing, and creates a "
            "threshold-based segmentation. See the "
            '<a href="https://github.com/aliu2298/SlicerSegmentationDemo">'
            "GitHub repository</a> for documentation."
        )
        self.parent.acknowledgementText = (
            "This module was developed as a work sample demonstrating "
            "3D Slicer scripted module development."
        )


# ---------------------------------------------------------------------------
# Widget (UI)
# ---------------------------------------------------------------------------
class SlicerSegmentationDemoWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Module panel UI with controls for loading data and running segmentation."""

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        # --- Data loading section ---
        dataCollapsible = slicer.qMRMLCollapsibleButton()
        dataCollapsible.text = "Sample Data"
        self.layout.addWidget(dataCollapsible)
        dataLayout = slicer.qt.QFormLayout(dataCollapsible)

        self.loadButton = slicer.qt.QPushButton("Load MRHead Sample Data")
        self.loadButton.toolTip = "Download and load the MRHead volume from Slicer sample data."
        self.loadButton.enabled = True
        dataLayout.addRow(self.loadButton)

        # --- Parameters section ---
        paramsCollapsible = slicer.qMRMLCollapsibleButton()
        paramsCollapsible.text = "Segmentation Parameters"
        self.layout.addWidget(paramsCollapsible)
        paramsLayout = slicer.qt.QFormLayout(paramsCollapsible)

        self.sigmaSlider = slicer.qMRMLSliderWidget()
        self.sigmaSlider.minimum = 0.1
        self.sigmaSlider.maximum = 5.0
        self.sigmaSlider.value = 1.0
        self.sigmaSlider.singleStep = 0.1
        self.sigmaSlider.toolTip = "Gaussian smoothing sigma (mm)."
        paramsLayout.addRow("Smoothing Sigma:", self.sigmaSlider)

        self.lowerThresholdSlider = slicer.qMRMLSliderWidget()
        self.lowerThresholdSlider.minimum = 0
        self.lowerThresholdSlider.maximum = 5000
        self.lowerThresholdSlider.value = 100
        self.lowerThresholdSlider.singleStep = 10
        self.lowerThresholdSlider.toolTip = "Lower intensity threshold for brain tissue."
        paramsLayout.addRow("Lower Threshold:", self.lowerThresholdSlider)

        self.upperThresholdSlider = slicer.qMRMLSliderWidget()
        self.upperThresholdSlider.minimum = 0
        self.upperThresholdSlider.maximum = 5000
        self.upperThresholdSlider.value = 3000
        self.upperThresholdSlider.singleStep = 10
        self.upperThresholdSlider.toolTip = "Upper intensity threshold for brain tissue."
        paramsLayout.addRow("Upper Threshold:", self.upperThresholdSlider)

        # --- Apply button ---
        self.applyButton = slicer.qt.QPushButton("Apply Segmentation")
        self.applyButton.toolTip = "Run smoothing and threshold segmentation."
        self.applyButton.enabled = True
        paramsLayout.addRow(self.applyButton)

        # --- Status label ---
        self.statusLabel = slicer.qt.QLabel("Status: Ready")
        self.layout.addWidget(self.statusLabel)

        # Vertical spacer
        self.layout.addStretch(1)

        # Connections
        self.loadButton.connect("clicked(bool)", self.onLoadData)
        self.applyButton.connect("clicked(bool)", self.onApplySegmentation)

        self.logic = SlicerSegmentationDemoLogic()

    def onLoadData(self):
        """Load MRHead sample data using Slicer's SampleData module."""
        self.statusLabel.text = "Status: Loading MRHead sample data..."
        slicer.app.processEvents()
        try:
            import SampleData
            self.volumeNode = SampleData.downloadSample("MRHead")
            slicer.util.setSliceViewerLayers(background=self.volumeNode)
            slicer.util.resetSliceViews()
            self.statusLabel.text = "Status: MRHead loaded successfully."
            logging.info("MRHead sample data loaded.")
        except Exception as e:
            self.statusLabel.text = f"Status: Error loading data - {e}"
            logging.error(f"Failed to load MRHead: {e}")

    def onApplySegmentation(self):
        """Run the segmentation workflow with current parameter values."""
        if not hasattr(self, "volumeNode") or self.volumeNode is None:
            self.statusLabel.text = "Status: Load sample data first."
            return

        self.statusLabel.text = "Status: Running segmentation..."
        slicer.app.processEvents()
        try:
            segNode = self.logic.runSegmentation(
                inputVolume=self.volumeNode,
                sigma=self.sigmaSlider.value,
                lowerThreshold=int(self.lowerThresholdSlider.value),
                upperThreshold=int(self.upperThresholdSlider.value),
            )
            self.statusLabel.text = "Status: Segmentation complete."
            logging.info("Segmentation applied successfully.")
        except Exception as e:
            self.statusLabel.text = f"Status: Error - {e}"
            logging.error(f"Segmentation failed: {e}")

    def cleanup(self):
        pass


# ---------------------------------------------------------------------------
# Logic (processing)
# ---------------------------------------------------------------------------
class SlicerSegmentationDemoLogic(ScriptedLoadableModuleLogic):
    """Processing logic: Gaussian smoothing followed by threshold segmentation."""

    def runSegmentation(self, inputVolume, sigma=1.0, lowerThreshold=100, upperThreshold=3000):
        """
        Run the segmentation pipeline.

        Steps:
        1. Apply Gaussian smoothing to reduce noise
        2. Create a threshold-based segmentation of brain tissue
        3. Display the segmentation overlay in slice views

        Returns the segmentation node.
        """
        import sitkUtils
        import SimpleITK as sitk

        logging.info(
            f"Running segmentation: sigma={sigma}, "
            f"threshold=[{lowerThreshold}, {upperThreshold}]"
        )

        # Pull volume into SimpleITK
        sitkImage = sitkUtils.PullVolumeFromSlicer(inputVolume)

        # Step 1: Gaussian smoothing
        smoothed = sitk.SmoothingRecursiveGaussian(sitkImage, sigma)

        # Step 2: Binary threshold
        segmented = sitk.BinaryThreshold(
            smoothed,
            lowerThreshold=lowerThreshold,
            upperThreshold=upperThreshold,
            insideValue=1,
            outsideValue=0,
        )

        # Push result back as a label map volume
        outputName = "BrainTissueSegmentation"
        existingNode = slicer.mrmlScene.GetFirstNodeByName(outputName)
        if existingNode:
            slicer.mrmlScene.RemoveNode(existingNode)

        labelMapNode = sitkUtils.PushVolumeToSlicer(segmented, None, outputName, "LabelMap")

        # Display label map as overlay in slice views
        slicer.util.setSliceViewerLayers(label=labelMapNode)

        logging.info("Segmentation complete.")
        return labelMapNode


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------
class SlicerSegmentationDemoTest(ScriptedLoadableModuleTest):
    """Basic self-test that runs the full workflow."""

    def runTest(self):
        self.setUp()
        self.test_FullWorkflow()

    def setUp(self):
        slicer.mrmlScene.Clear()

    def test_FullWorkflow(self):
        """Test: load MRHead, run segmentation, verify output exists."""
        self.delayDisplay("Starting full workflow test...")

        # Load sample data
        import SampleData
        volumeNode = SampleData.downloadSample("MRHead")
        self.assertIsNotNone(volumeNode, "MRHead volume should load successfully.")

        # Run segmentation
        logic = SlicerSegmentationDemoLogic()
        resultNode = logic.runSegmentation(
            inputVolume=volumeNode,
            sigma=1.0,
            lowerThreshold=100,
            upperThreshold=3000,
        )
        self.assertIsNotNone(resultNode, "Segmentation output should exist.")

        self.delayDisplay("Full workflow test passed.")
