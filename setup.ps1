Write-Host "Setting up File Integrity Monitoring System..."

python -m venv .venv

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    .\.venv\Scripts\Activate.ps1
}

pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete."
Write-Host "Run the project using:"
Write-Host "python monitor.py"
