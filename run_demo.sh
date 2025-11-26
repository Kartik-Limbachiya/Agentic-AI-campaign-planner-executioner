#!/bin/bash
# Demo Script for Agentic AI Campaign Planner & Executioner
# Run this script to execute all demo scenarios

echo "🤖 Agentic AI Campaign Planner & Executioner - Demo Script"
echo "=========================================================="
echo ""
echo "This script will run all demo scenarios for the POC."
echo "Demo Date: December 2, 2024"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cd "$(dirname "$0")"

# Function to run demo
run_demo() {
    local demo_name=$1
    local demo_cmd=$2
    
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Running: $demo_name${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
    echo ""
    
    python main.py $demo_cmd
    
    echo ""
    echo -e "${GREEN}✓ $demo_name completed${NC}"
    echo ""
}

# Show available demos
echo "Available Demos:"
echo "1. Quick Demo (No API Key Required) - Recommended for immediate testing"
echo "2. Demo 1 - Tech Product Launch Campaign"
echo "3. Demo 2 - E-commerce Holiday Campaign"
echo "4. Interactive Mode - Create custom campaign"
echo ""
echo "Select demo to run (1-4) or 'all' for all demos:"
read -p "Enter choice: " choice

case $choice in
    1)
        run_demo "Quick Demo (No API Key)" "quick"
        ;;
    2)
        run_demo "Demo 1: Tech Product Launch" "demo1"
        ;;
    3)
        run_demo "Demo 2: E-commerce Holiday Campaign" "demo2"
        ;;
    4)
        run_demo "Interactive Campaign Creation" "interactive"
        ;;
    all)
        run_demo "Quick Demo (No API Key)" "quick"
        run_demo "Demo 1: Tech Product Launch" "demo1"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Demo execution completed!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo "Generated files are in the 'outputs/' directory:"
ls -lh outputs/
