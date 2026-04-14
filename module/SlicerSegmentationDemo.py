"""SlicerSegmentationDemo - Automated Brain Tissue Segmentation Module

This is a 3D Slicer scripted module that demonstrates a professional-grade brain
tissue segmentation workflow with input validation, morphological post-processing,
and comprehensive error handling.

Module structure follows the standard Slicer scripted module pattern:
- SlicerSegmentationDemo: Module descriptor (metadata, icon, help text)
- SlicerSegmentationDemoWidget: UI panel with parameter controls
- SlicerSegmentationDemoLogic: Processing logic (smoothing, thresholding, morphology)
- SlicerSegmentationDemoTest: Comprehensive self-test with edge cases
"""

import logging
import time
import slicer
from slicer.ScriptedLoadableModule import (
    ScriptedLoadableModule,
    ScriptedLoadableModuleWidget,
    ScriptedLoadableModuleLogic,
    ScriptedLoadableModuleTest,
)
from slicer.util import VTKObservationMixin

# Configure logging with timestamps
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s - %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


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
            "Automated brain tissue segmentation with validation and morphological post-processing. "
            "Load the MRHead sample dataset or provide your own volume, apply Gaussian smoothing, "
            "threshold-based segmentation, and optional morphological operations (closing, erosion, dilation). "
            "Features include input validation, error handling, and execution timing. "
            'See the <a href="https://github.com/aliu2298/SlicerSegmentationDemo">'
            "GitHub repository</a> for documentation."
        )
        self.parent.acknowledgementText = (
            "This module was developed as a work sample demonstrating professional-grade "
            "3D Slicer scripted module development with robust error handling."
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
        dataCollapsible.text = "Input Volume"
        self.layout.addWidget(dataCollapsible)
        dataLayout = slicer.qt.QFormLayout(dataCollapsible)

        self.loadButton = slicer.qt.QPushButton("Load MRHead Sample Data")
        self.loadButton.toolTip = "Download and load the MRHead volume from Slicer sample data."
        self.loadButton.enabled = True
        dataLayout.addRow(self.loadButton)

        # Volume selector for custom input
        self.volumeSelector = slicer.qMRMLNodeComboBox()
        self.volumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.volumeSelector.selectNodeUponCreation = False
        self.volumeSelector.addEnabled = False
        self.volumeSelector.removeEnabled = False
        self.volumeSelector.noneDisplay = "-- Select a volume --"
        self.volumeSelector.setMRMLScene(slicer.mrmlScene)
        self.volumeSelector.toolTip = "Select a volume from the scene to segment."
        dataLayout.addRow("Or select volume:", self.volumeSelector)

        # --- Parameters section ---
        paramsCollapsible = slicer.qMRMLCollapsibleButton()
        paramsCollapsible.text = "Segmentation Parameters"
        self.layout.addWidget(paramsCollapsible)
        paramsLayout = slicer.qt.QFormLayout(paramsCollapsible)

        # Smoothing sigma
        self.sigmaSlider = slicer.qMRMLSliderWidget()
        self.sigmaSlider.minimum = 0.0
        self.sigmaSlider.maximum = 5.0
        self.sigmaSlider.value = 1.0
        self.sigmaSlider.singleStep = 0.1
        self.sigmaSlider.toolTip = "Gaussian smoothing sigma (mm). 0 = no smoothing."
        paramsLayout.addRow("Smoothing Sigma:", self.sigmaSlider)

        # Lower threshold
        self.lowerThresholdSlider = slicer.qMRMLSliderWidget()
        self.lowerThresholdSlider.minimum = 0
        self.lowerThresholdSlider.maximum = 5000
        self.lowerThresholdSlider.value = 100
        self.lowerThresholdSlider.singleStep = 10
        self.lowerThresholdSlider.toolTip = "Lower intensity threshold for brain tissue."
        paramsLayout.addRow("Lower Threshold:", self.lowerThresholdSlider)

        # Upper threshold
        self.upperThresholdSlider = slicer.qMRMLSliderWidget()
        self.upperThresholdSlider.minimum = 0
        self.upperThresholdSlider.maximum = 5000
        self.upperThresholdSlider.value = 3000
        self.upperThresholdSlider.singleStep = 10
        self.upperThresholdSlider.toolTip = "Upper intensity threshold for brain tissue."
        paramsLayout.addRow("Upper Threshold:", self.upperThresholdSlider)

        # --- Post-processing section ---
        postProcessCollapsible = slicer.qMRMLCollapsibleButton()
        postProcessCollapsible.text = "Post-Processing"
        self.layout.addWidget(postProcessCollapsible)
        postProcessLayout = slicer.qt.QFormLayout(postProcessCollapsible)

        self.closingCheckBox = slicer.qt.QCheckBox()
        self.closingCheckBox.checked = True
        self.closingCheckBox.toolTip = "Apply morphological closing to remove small holes."
        postProcessLayout.addRow("Morphological Closing:", self.closingCheckBox)

        self.erosionCheckBox = slicer.qt.QCheckBox()
        self.erosionCheckBox.checked = False
        self.erosionCheckBox.toolTip = "Apply erosion to remove small islands."
        postProcessLayout.addRow("Morphological Erosion:", self.erosionCheckBox)

        self.radiusSpinBox = slicer.qt.QSpinBox()
        self.radiusSpinBox.minimum = 1
        self.radiusSpinBox.maximum = 5
        self.radiusSpinBox.value = 1
        self.radiusSpinBox.toolTip = "Radius in voxels for morphological operations."
        postProcessLayout.addRow("Morphology Radius:", self.radiusSpinBox)

        # --- Apply button ---
        self.applyButton = slicer.qt.QPushButton("Apply Segmentation")
        self.applyButton.toolTip = "Run smoothing, threshold, and optional morphological operations."
        self.applyButton.enabled = True
        paramsLayout.addRow(self.applyButton)

        # --- Status label ---
        self.statusLabel = slicer.qt.QLabel("Status: Ready")
        self.statusLabel.setStyleSheet("QLabel { color: green; font-weight: bold; }")
        self.layout.addWidget(self.statusLabel)

        # Vertical spacer
        self.layout.addStretch(1)

        # Connections
        self.loadButton.connect("clicked(bool)", self.onLoadData)
        self.applyButton.connect("clicked(bool)", self.onApplySegmentation)

        self.logic = SlicerSegmentationDemoLogic()
        self.volumeNode = None

    def updateStatus(self, message, isError=False):
        """Update status label with optional error coloring."""
        self.statusLabel.setText(f"Status: {message}")
        if isError:
            self.statusLabel.setStyleSheet("QLabel { color: red; font-weight: bold; }")
        else:
            self.statusLabel.setStyleSheet("QLabel { color: green; font-weight: bold; }")
        slicer.app.processEvents()

    def onLoadData(self):
        """Load MRHead sample data using Slicer's SampleData module."""
        self.updateStatus("Loading MRHead sample data...")
        try:
            import SampleData
            logger.debug("Downloading MRHead sample data...")
            self.volumeNode = SampleData.downloadSample("MRHead")
            self.volumeSelector.setCurrentNode(self.volumeNode)
            slicer.util.setSliceViewerLayers(background=self.volumeNode)
            slicer.util.resetSliceViews()
            self.updateStatus("MRHead loaded successfully.")
            logger.info("MRHead sample data loaded and displayed.")
        except Exception as e:
            self.updateStatus(f"Error loading data: {str(e)}", isError=True)
            logger.error(f"Failed to load MRHead: {e}", exc_info=True)

    def onApplySegmentation(self):
        """Run the segmentation workflow with current parameter values."""
        # Get input volume (prioritize selector, fall back to loaded volume)
        inputVolume = self.volumeSelector.currentNode()
        if inputVolume is None:
            inputVolume = self.volumeNode if hasattr(self, "volumeNode") else None

        if inputVolume is None:
            self.updateStatus("Load or select a volume first.", isError=True)
            logger.warning("Segmentation attempted without input volume.")
            return

        self.updateStatus("Running segmentation...")
        try:
            start_time = time.time()
            logger.debug(f"Starting segmentation on volume: {inputVolume.GetName()}")
            logger.debug(f"Parameters: sigma={self.sigmaSlider.value}, "
                        f"threshold=[{int(self.lowerThresholdSlider.value)}, {int(self.upperThresholdSlider.value)}]")

            segNode = self.logic.runSegmentation(
                inputVolume=inputVolume,
                sigma=self.sigmaSlider.value,
                lowerThreshold=int(self.lowerThresholdSlider.value),
                upperThreshold=int(self.upperThresholdSlider.value),
                applyClosing=self.closingCheckBox.checked,
                applyErosion=self.erosionCheckBox.checked,
                morphRadius=self.radiusSpinBox.value,
            )

            elapsed = time.time() - start_time
            self.updateStatus(f"Segmentation complete ({elapsed:.2f}s).")
            logger.info(f"Segmentation completed successfully in {elapsed:.2f} seconds.")
        except ValueError as e:
            self.updateStatus(f"Invalid parameters: {str(e)}", isError=True)
            logger.error(f"Parameter validation error: {e}")
        except Exception as e:
            self.updateStatus(f"Segmentation failed: {str(e)}", isError=True)
            logger.error(f"Segmentation error: {e}", exc_info=True)

    def cleanup(self):
        pass


# ---------------------------------------------------------------------------
# Logic (processing)
# ---------------------------------------------------------------------------
class SlicerSegmentationDemoLogic(ScriptedLoadableModuleLogic):
    """Processing logic: Gaussian smoothing, threshold segmentation, and morphological operations."""

    def _validate_parameters(self, inputVolume, sigma, lowerThreshold, upperThreshold, morphRadius):
        """
        Validate input parameters. Raises ValueError with descriptive messages.

        Args:
            inputVolume: Input volume node to validate
            sigma: Gaussian smoothing sigma
            lowerThreshold: Lower threshold value
            upperThreshold: Upper threshold value
            morphRadius: Morphological operation radius

        Raises:
            ValueError: If any parameter is invalid
        """
        if inputVolume is None:
            raise ValueError("Input volume is None.")

        if inputVolume.GetImageData() is None:
            raise ValueError(f"Volume '{inputVolume.GetName()}' has no image data.")

        if sigma < 0:
            raise ValueError(f"Smoothing sigma must be >= 0, got {sigma}.")

        if lowerThreshold >= upperThreshold:
            raise ValueError(
                f"Lower threshold ({lowerThreshold}) must be < upper threshold ({upperThreshold})."
            )

        if morphRadius < 1:
            raise ValueError(f"Morphology radius must be >= 1, got {morphRadius}.")

        logger.debug("Parameter validation passed.")

    def runSegmentation(
        self,
        inputVolume,
        sigma=1.0,
        lowerThreshold=100,
        upperThreshold=3000,
        applyClosing=True,
        applyErosion=False,
        morphRadius=1,
    ):
        """
        Run the complete segmentation pipeline.

        Pipeline steps:
        1. Validate inputs
        2. Apply Gaussian smoothing to reduce noise
        3. Create threshold-based segmentation of brain tissue
        4. Apply optional morphological post-processing (closing, erosion)
        5. Push result back to Slicer scene and display

        Args:
            inputVolume: Input vtkMRMLScalarVolumeNode
            sigma: Gaussian smoothing sigma in mm (0 = no smoothing)
            lowerThreshold: Lower intensity threshold
            upperThreshold: Upper intensity threshold
            applyClosing: Whether to apply morphological closing
            applyErosion: Whether to apply morphological erosion
            morphRadius: Radius in voxels for morphological operations

        Returns:
            Output vtkMRMLLabelMapVolumeNode

        Raises:
            ValueError: If parameters are invalid
            RuntimeError: If processing fails
        """
        import sitkUtils
        import SimpleITK as sitk

        # Validate all parameters
        self._validate_parameters(inputVolume, sigma, lowerThreshold, upperThreshold, morphRadius)

        logger.info(
            f"Starting segmentation on volume '{inputVolume.GetName()}': "
            f"sigma={sigma}, threshold=[{lowerThreshold}, {upperThreshold}], "
            f"closing={applyClosing}, erosion={applyErosion}, morphRadius={morphRadius}"
        )

        step_start = time.time()

        try:
            # Pull volume into SimpleITK
            logger.debug("Step 1: Converting volume to SimpleITK...")
            sitkImage = sitkUtils.PullVolumeFromSlicer(inputVolume)
            logger.debug(f"  Image size: {sitkImage.GetSize()}, "
                        f"spacing: {sitkImage.GetSpacing()}, "
                        f"dtype: {sitkImage.GetPixelIDTypeAsString()}")

            # Step 1: Gaussian smoothing (optional)
            if sigma > 0:
                logger.debug(f"Step 2: Applying Gaussian smoothing (sigma={sigma})...")
                smoothed = sitk.SmoothingRecursiveGaussian(sitkImage, sigma)
                logger.debug("  Smoothing complete.")
            else:
                logger.debug("Step 2: Skipping smoothing (sigma=0).")
                smoothed = sitkImage

            # Step 2: Binary threshold
            logger.debug(
                f"Step 3: Applying threshold segmentation "
                f"[{lowerThreshold}, {upperThreshold}]..."
            )
            segmented = sitk.BinaryThreshold(
                smoothed,
                lowerThreshold=lowerThreshold,
                upperThreshold=upperThreshold,
                insideValue=1,
                outsideValue=0,
            )
            logger.debug("  Thresholding complete.")

            # Step 3: Optional morphological post-processing
            if applyClosing or applyErosion:
                logger.debug("Step 4: Applying morphological operations...")

                if applyClosing:
                    logger.debug(f"  Applying closing (radius={morphRadius})...")
                    kernel = sitk.sitkBall
                    segmented = sitk.BinaryMorphologicalClosing(
                        segmented, morphRadius, kernel
                    )
                    logger.debug("    Closing complete.")

                if applyErosion:
                    logger.debug(f"  Applying erosion (radius={morphRadius})...")
                    kernel = sitk.sitkBall
                    segmented = sitk.BinaryErode(segmented, morphRadius, kernel)
                    logger.debug("    Erosion complete.")
            else:
                logger.debug("Step 4: Skipping morphological operations.")

            # Step 4: Push result back to Slicer
            logger.debug("Step 5: Converting result back to Slicer...")
            outputName = "BrainTissueSegmentation"
            existingNode = slicer.mrmlScene.GetFirstNodeByName(outputName)
            if existingNode:
                logger.debug(f"  Removing existing node '{outputName}'...")
                slicer.mrmlScene.RemoveNode(existingNode)

            labelMapNode = sitkUtils.PushVolumeToSlicer(
                segmented, None, outputName, "LabelMap"
            )
            logger.debug(f"  Created label map node: {labelMapNode.GetName()}")

            # Display label map as overlay in slice views
            slicer.util.setSliceViewerLayers(label=labelMapNode)
            logger.debug("  Label map displayed in slice views.")

            elapsed = time.time() - step_start
            logger.info(f"Segmentation completed successfully in {elapsed:.3f} seconds.")
            return labelMapNode

        except Exception as e:
            logger.error(f"Segmentation failed: {e}", exc_info=True)
            raise RuntimeError(f"Segmentation processing failed: {e}")


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------
class SlicerSegmentationDemoTest(ScriptedLoadableModuleTest):
    """Comprehensive self-tests including edge cases and parameter validation."""

    def runTest(self):
        self.setUp()
        self.test_FullWorkflow()
        self.test_ParameterValidation()
        self.test_MorphologicalOperations()

    def setUp(self):
        slicer.mrmlScene.Clear()

    def test_FullWorkflow(self):
        """Test: load MRHead, run segmentation with defaults, verify output."""
        self.delayDisplay("Test 1: Full workflow with default parameters...")

        # Load sample data
        import SampleData
        volumeNode = SampleData.downloadSample("MRHead")
        self.assertIsNotNone(volumeNode, "MRHead volume should load successfully.")
        self.assertIsNotNone(
            volumeNode.GetImageData(),
            "MRHead volume should have valid image data."
        )

        # Run segmentation
        logic = SlicerSegmentationDemoLogic()
        resultNode = logic.runSegmentation(
            inputVolume=volumeNode,
            sigma=1.0,
            lowerThreshold=100,
            upperThreshold=3000,
            applyClosing=True,
            applyErosion=False,
            morphRadius=1,
        )
        self.assertIsNotNone(resultNode, "Segmentation output should exist.")
        self.assertIsNotNone(
            resultNode.GetImageData(),
            "Segmentation output should have valid image data."
        )
        self.assertEqual(
            resultNode.GetName(),
            "BrainTissueSegmentation",
            "Output node should be named 'BrainTissueSegmentation'."
        )

        # Verify output is label map
        self.assertTrue(
            resultNode.IsA("vtkMRMLLabelMapVolumeNode"),
            "Output should be a label map volume node."
        )

        self.delayDisplay("Test 1 PASSED.")

    def test_ParameterValidation(self):
        """Test: parameter validation catches invalid inputs."""
        self.delayDisplay("Test 2: Parameter validation...")

        import SampleData
        volumeNode = SampleData.downloadSample("MRHead")
        logic = SlicerSegmentationDemoLogic()

        # Test: lowerThreshold >= upperThreshold
        with self.assertRaises(ValueError):
            logic.runSegmentation(
                inputVolume=volumeNode,
                sigma=1.0,
                lowerThreshold=3000,
                upperThreshold=100,  # Invalid: lower > upper
            )
        logger.info("Validation test 1 passed: threshold reversal detected.")

        # Test: negative sigma
        with self.assertRaises(ValueError):
            logic.runSegmentation(
                inputVolume=volumeNode,
                sigma=-1.0,  # Invalid: negative sigma
                lowerThreshold=100,
                upperThreshold=3000,
            )
        logger.info("Validation test 2 passed: negative sigma detected.")

        # Test: invalid morphRadius
        with self.assertRaises(ValueError):
            logic.runSegmentation(
                inputVolume=volumeNode,
                sigma=1.0,
                lowerThreshold=100,
                upperThreshold=3000,
                morphRadius=0,  # Invalid: radius < 1
            )
        logger.info("Validation test 3 passed: invalid morphRadius detected.")

        # Test: None input volume
        with self.assertRaises(ValueError):
            logic.runSegmentation(
                inputVolume=None,
                sigma=1.0,
                lowerThreshold=100,
                upperThreshold=3000,
            )
        logger.info("Validation test 4 passed: None volume detected.")

        self.delayDisplay("Test 2 PASSED.")

    def test_MorphologicalOperations(self):
        """Test: morphological closing and erosion produce valid output."""
        self.delayDisplay("Test 3: Morphological operations...")

        import SampleData
        volumeNode = SampleData.downloadSample("MRHead")
        logic = SlicerSegmentationDemoLogic()

        # Test with closing enabled
        logger.info("Testing with morphological closing...")
        resultWithClosing = logic.runSegmentation(
            inputVolume=volumeNode,
            sigma=1.0,
            lowerThreshold=100,
            upperThreshold=3000,
            applyClosing=True,
            applyErosion=False,
            morphRadius=1,
        )
        self.assertIsNotNone(resultWithClosing, "Closing should produce output.")
        logger.info("Closing test passed.")

        # Remove the output node
        slicer.mrmlScene.RemoveNode(resultWithClosing)

        # Test with erosion enabled
        logger.info("Testing with morphological erosion...")
        resultWithErosion = logic.runSegmentation(
            inputVolume=volumeNode,
            sigma=1.0,
            lowerThreshold=100,
            upperThreshold=3000,
            applyClosing=False,
            applyErosion=True,
            morphRadius=1,
        )
        self.assertIsNotNone(resultWithErosion, "Erosion should produce output.")
        logger.info("Erosion test passed.")

        # Remove the output node
        slicer.mrmlScene.RemoveNode(resultWithErosion)

        # Test without smoothing (sigma=0)
        logger.info("Testing without smoothing...")
        resultNoSmoothing = logic.runSegmentation(
            inputVolume=volumeNode,
            sigma=0.0,
            lowerThreshold=100,
            upperThreshold=3000,
            applyClosing=True,
            applyErosion=False,
            morphRadius=1,
        )
        self.assertIsNotNone(resultNoSmoothing, "Segmentation without smoothing should work.")
        logger.info("No-smoothing test passed.")

        self.delayDisplay("Test 3 PASSED.")
