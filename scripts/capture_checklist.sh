#!/bin/bash
# Screenshot Capture Checklist
# Run through this checklist while capturing screenshots for SlicerSegmentationDemo

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  SlicerSegmentationDemo - Screenshot Capture Checklist         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

FILES_TO_CAPTURE=(
    "screenshots/main-workflow.png"
    "screenshots/segmentation-view.png"
    "screenshots/demo.gif"
)

COMPLETED=()

show_menu() {
    echo ""
    echo "Status of captures:"
    echo "==================="
    for i in "${!FILES_TO_CAPTURE[@]}"; do
        file="${FILES_TO_CAPTURE[$i]}"
        if [[ " ${COMPLETED[@]} " =~ " $i " ]]; then
            echo "  [✓] $file"
        else
            echo "  [ ] $file"
        fi
    done
    echo ""
    echo "Options:"
    echo "--------"
    echo "  1) Start capture: main-workflow.png"
    echo "  2) Start capture: segmentation-view.png"
    echo "  3) Start capture: demo.gif"
    echo "  4) View detailed instructions"
    echo "  5) Check file status"
    echo "  6) Exit"
    echo ""
}

capture_main_workflow() {
    echo ""
    echo "📸 Capturing: main-workflow.png"
    echo "────────────────────────────────────────"
    echo "Instructions:"
    echo "  1. In Slicer, click \"Load MRHead Sample Data\""
    echo "  2. Wait 3-5 seconds for data to load"
    echo "  3. Ensure module panel is visible on LEFT side"
    echo "  4. All parameter sliders should be visible"
    echo "  5. Take screenshot (Cmd+Shift+4 on macOS, or Edit > Take Screenshot)"
    echo "  6. Save to: screenshots/main-workflow.png"
    echo ""
    echo "Verification:"
    echo "  ✓ Module panel fully visible"
    echo "  ✓ Four slice views showing MRHead (grayscale)"
    echo "  ✓ Status shows 'MRHead loaded successfully'"
    echo "  ✓ Image is sharp and well-lit"
    echo ""
    read -p "Press Enter when capture is complete..."
    if check_file "screenshots/main-workflow.png"; then
        COMPLETED+=(0)
    fi
}

capture_segmentation_view() {
    echo ""
    echo "📸 Capturing: segmentation-view.png"
    echo "────────────────────────────────────────"
    echo "Instructions:"
    echo "  1. With MRHead already loaded, click \"Apply Segmentation\""
    echo "  2. Wait 2-3 seconds for processing"
    echo "  3. Status should show 'Segmentation complete'"
    echo "  4. Scroll through slices to find clear brain tissue segmentation"
    echo "  5. Take screenshot showing colored segmentation overlay"
    echo "  6. Save to: screenshots/segmentation-view.png"
    echo ""
    echo "Verification:"
    echo "  ✓ Brain tissue regions clearly segmented (colored overlay)"
    echo "  ✓ Overlay color is distinct and visible"
    echo "  ✓ Multiple slice views show segmentation"
    echo "  ✓ No errors or artifacts visible"
    echo ""
    read -p "Press Enter when capture is complete..."
    if check_file "screenshots/segmentation-view.png"; then
        COMPLETED+=(1)
    fi
}

capture_demo_gif() {
    echo ""
    echo "🎬 Capturing: demo.gif (Optional but recommended)"
    echo "────────────────────────────────────────"
    echo "Instructions:"
    echo "  1. Start screen recording (Gifox, LICEcap, or QuickTime)"
    echo "  2. Select Module > Examples > SlicerSegmentationDemo (~3 sec)"
    echo "  3. Click \"Load MRHead Sample Data\" (~5 sec)"
    echo "  4. Review parameters (~2 sec)"
    echo "  5. Click \"Apply Segmentation\" (~3 sec)"
    echo "  6. Scroll through slices to show results (~5 sec)"
    echo ""
    echo "  Total time: ~20 seconds"
    echo ""
    echo "After recording, convert to GIF:"
    echo "  macOS: ffmpeg -i recording.mov -vf \"fps=10,scale=900:-1\" -loop 0 -c:v gif demo.gif"
    echo "  Then: cp demo.gif screenshots/"
    echo ""
    read -p "Press Enter when GIF is saved..."
    if check_file "screenshots/demo.gif"; then
        COMPLETED+=(2)
    fi
}

check_file() {
    if [ -f "$1" ]; then
        echo "  ✓ Found: $1 ($(ls -lh "$1" | awk '{print $5}'))"
        return 0
    else
        echo "  ✗ Not found: $1"
        return 1
    fi
}

view_instructions() {
    if [ -f "scripts/capture_screenshots.md" ]; then
        less scripts/capture_screenshots.md
    elif [ -f "screenshots/README.md" ]; then
        less screenshots/README.md
    else
        echo "No instruction files found!"
    fi
}

check_status() {
    echo ""
    echo "File Status:"
    echo "────────────"
    for file in "${FILES_TO_CAPTURE[@]}"; do
        check_file "$file"
    done
    echo ""
}

# Main loop
while true; do
    show_menu
    read -p "Enter choice (1-6): " choice
    
    case $choice in
        1) capture_main_workflow ;;
        2) capture_segmentation_view ;;
        3) capture_demo_gif ;;
        4) view_instructions ;;
        5) check_status ;;
        6) 
            echo ""
            echo "Thank you for capturing screenshots!"
            echo "Don't forget to:"
            echo "  1. Commit the files: git add screenshots/ && git commit -m '...'"
            echo "  2. Push to GitHub: git push"
            echo ""
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
done
