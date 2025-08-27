#!/bin/bash
# Script to extract CCS firmware from Thorlabs OSA software

set -e  # Exit immediately if a command fails

# Install innoextract if not already installed
if ! command -v innoextract &> /dev/null; then
    echo "Installing innoextract..."
    sudo apt update
    sudo apt install -y innoextract
fi

# Download the Thorlabs OSA installer
echo "Downloading Thorlabs OSA installer..."
curl -O https://www.thorlabs.com/software/THO/OSA/V2_90/ThorlabsOSASW_Full_setup.exe

# Create necessary directories
mkdir -p ccs_firmware temp_extract

# Extract only the CCS .spt files
echo "Extracting CCS firmware..."
innoextract --extract --output-dir=temp_extract \
--include "app/CCS/inf/Loader/CCS100.spt" \
--include "app/CCS/inf/Loader/CCS125.spt" \
--include "app/CCS/inf/Loader/CCS150.spt" \
--include "app/CCS/inf/Loader/CCS175.spt" \
--include "app/CCS/inf/Loader/CCS200.spt" \
ThorlabsOSASW_Full_setup.exe

# Move firmware files to final folder
mv temp_extract/app/CCS/inf/Loader/CCS*.spt ccs_firmware/

# Clean up
rm -rf temp_extract ThorlabsOSASW_Full_setup.exe

echo "Firmware extraction complete. Files are in ccs_firmware/"
