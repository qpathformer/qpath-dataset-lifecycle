# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: setup_examples.ps1
# Description: Reference tooling for governed dataset lifecycle workflows

# setup_examples.ps1
# Copies canonical ID_3 freeze artifacts into the repo examples folder

$ErrorActionPreference = "Stop"

# Destination repo example folder
$destination = "C:\v1.0-governed-dataset-lifecycle\examples\id3_freeze_example"

# Expected files in an ID_3 freeze folder
$requiredFiles = @(
    "hashes.txt",
    "ID3_FREEZE_NOTE.md",
    "module_03_baseline.canonical.json",
    "module_03_variant.canonical.json",
    "session_baseline.canonical.json",
    "session_variant.canonical.json"
)

$source = Get-Location

Write-Host ""
Write-Host "Source freeze folder:" $source
Write-Host "Destination folder :" $destination
Write-Host ""

# Ensure destination exists
if (-not (Test-Path $destination)) {
    New-Item -ItemType Directory -Force -Path $destination | Out-Null
}

# Validate required files
foreach ($file in $requiredFiles) {
    if (-not (Test-Path (Join-Path $source $file))) {
        Write-Error "Missing required freeze artifact: $file"
        exit 1
    }
}

# Copy files
robocopy `
    $source `
    $destination `
    $requiredFiles `
    /NFL /NDL /NJH /NJS /NC /NS /NP | Out-Null

Write-Host "Copied canonical ID_3 freeze artifacts:"
Get-ChildItem $destination | Select-Object Name, Length, LastWriteTime

Write-Host ""
Write-Host "ID_3 freeze example setup complete."