# Installation Script for Video Interview Feature
# Run this in PowerShell

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "HR Agent - Video Interview Feature Installation" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Upgrade pip
Write-Host "[1/4] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 2: Install requirements
Write-Host ""
Write-Host "[2/4] Installing required packages..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Gray
pip install -r requirements.txt

# Step 3: Create upload directory
Write-Host ""
Write-Host "[3/4] Creating upload directory..." -ForegroundColor Yellow
if (-not (Test-Path "uploads\interview_videos")) {
    New-Item -ItemType Directory -Path "uploads\interview_videos" -Force | Out-Null
    Write-Host "Created: uploads\interview_videos" -ForegroundColor Green
} else {
    Write-Host "Directory already exists: uploads\interview_videos" -ForegroundColor Green
}

# Step 4: Verify installation
Write-Host ""
Write-Host "[4/4] Verifying installation..." -ForegroundColor Yellow

$packages = @("streamlit", "opencv-python", "librosa", "moviepy", "fer", "groq", "PyPDF2")
$allInstalled = $true

foreach ($package in $packages) {
    $installed = pip show $package 2>$null
    if ($installed) {
        Write-Host "✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "✗ $package NOT installed" -ForegroundColor Red
        $allInstalled = $false
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan

if ($allInstalled) {
    Write-Host "Installation completed successfully! ✓" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Make sure you have GROQ_API_KEY in .env file" -ForegroundColor White
    Write-Host "2. Run: streamlit run app.py" -ForegroundColor White
    Write-Host "3. Test the video interview feature!" -ForegroundColor White
} else {
    Write-Host "Installation completed with some errors!" -ForegroundColor Red
    Write-Host "Please check the errors above and try:" -ForegroundColor Yellow
    Write-Host "pip install -r requirements.txt" -ForegroundColor White
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
