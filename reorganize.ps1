# PowerShell script to reorganize the zebra_puzzle project
# Run this from the zebra_puzzle directory

Write-Host "Starting Project Reorganization..." -ForegroundColor Green
Write-Host ""

# Create backup
Write-Host "Creating backup..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "backup_$timestamp"
New-Item -ItemType Directory -Path $backupDir -ErrorAction SilentlyContinue

# Function to safely move file
function Move-SafelyIfExists {
    param($source, $destination)
    if (Test-Path $source) {
        Write-Host "  Moving $source to $destination" -ForegroundColor Cyan
        Move-Item -Path $source -Destination $destination -Force
        return $true
    }
    return $false
}

# Function to safely copy file
function Copy-SafelyIfExists {
    param($source, $destination)
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $destination -Force
        return $true
    }
    return $false
}

# Ensure directories exist
Write-Host ""
Write-Host "Creating directory structure..." -ForegroundColor Yellow
$dirs = @("data", "data\generated", "results", "docs", "examples", "src")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    }
}

# Move data files
Write-Host ""
Write-Host "Moving data files..." -ForegroundColor Yellow
Move-SafelyIfExists "attribute_entity.json" "data\"
Move-SafelyIfExists "numbered_entity.json" "data\"
Move-SafelyIfExists "sample_puzzle.json" "data\"
Move-SafelyIfExists "single_puzzle_8000.json" "data\"
Move-SafelyIfExists "zebra_puzzles_gurobi_100.json" "data\generated\"

# Move result files
Write-Host ""
Write-Host "Moving result files..." -ForegroundColor Yellow
Get-ChildItem -Filter "llm_test_results_*.json" | ForEach-Object {
    Move-SafelyIfExists $_.Name "results\"
}
Get-ChildItem -Filter "puzzle_*_result.json" | ForEach-Object {
    Move-SafelyIfExists $_.Name "results\"
}
Get-ChildItem -Filter "*.log" | ForEach-Object {
    Move-SafelyIfExists $_.Name "results\"
}

# Move documentation
Write-Host ""
Write-Host "Moving documentation..." -ForegroundColor Yellow
$docFiles = @(
    "LLM_TESTING_GUIDE.md",
    "QUICK_START_GUIDE.md",
    "CODE_UPDATE_SUMMARY.md",
    "COMPLETE_DELIVERY_SUMMARY.md",
    "EVALUATION_SUMMARY.md",
    "SINGLE_PUZZLE_EXAMPLE.md",
    "LLM_TEST_REPORT.md",
    "REORGANIZATION_GUIDE.md"
)
foreach ($file in $docFiles) {
    Move-SafelyIfExists $file "docs\"
}

# Move example files
Write-Host ""
Write-Host "Moving example files..." -ForegroundColor Yellow
Move-SafelyIfExists "example_llm_test.py" "examples\"

# Copy source files to src/ (keep originals for now)
Write-Host ""
Write-Host "Copying source files to src/ (originals kept)..." -ForegroundColor Yellow
Copy-SafelyIfExists "zebra_abs_pro.py" "src\puzzle_generator.py"
Copy-SafelyIfExists "generate_100_with_gurobi.py" "src\batch_generator.py"
Copy-SafelyIfExists "test_llm_on_puzzles.py" "src\llm_tester.py"
Copy-SafelyIfExists "analyze_puzzles.py" "src\puzzle_analyzer.py"
Copy-SafelyIfExists "prompt_formatting.py" "src\prompt_formatter.py"

# Create __init__.py in src
Write-Host ""
Write-Host "Creating __init__.py files..." -ForegroundColor Yellow
$initContent = @"
"""
Zebra Puzzle Generator - Source Package

Core modules for generating and testing zebra logic puzzles.
"""

__version__ = '1.0.0'
"@
Set-Content -Path "src\__init__.py" -Value $initContent

# Create summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Reorganization Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "New Structure:" -ForegroundColor Yellow
Write-Host "  data/        - JSON data files and generated puzzles"
Write-Host "  results/     - Test results and logs"
Write-Host "  docs/        - Documentation files"
Write-Host "  examples/    - Example scripts"
Write-Host "  src/         - Source code (new organization)"
Write-Host "  tests/       - Unit tests (unchanged)"
Write-Host ""
Write-Host "Original Python files kept in root directory for backward compatibility" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test that scripts still work"
Write-Host "  2. Update import paths if using src/ files"
Write-Host "  3. Remove original files from root once verified"
Write-Host ""
