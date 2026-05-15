# 🧬 WINDOWS PRE-FLIGHT CHECK: SOVEREIGN DEPLOYMENT
# Verifies environment for Workstation vΩ∞-OMNISYNTHESIS-SUPREME

Write-Host "🔍 Validating Windows environment for Supreme Convergence..." -ForegroundColor Cyan

# 1. Check PowerShell Version
if ($PSVersionTable.PSVersion.Major -lt 5) {
    Write-Error "PowerShell 5.1 or 7+ is required. Please update."
    exit 1
}
Write-Host "✅ PowerShell version verified." -ForegroundColor Green

# 2. Check WSL2
$wslStatus = wsl --status 2>$null
if (-not $wslStatus) {
    Write-Warning "WSL2 not detected. Attempting to check if feature is enabled..."
    $feature = Get-WindowsOptionalFeature -Online -FeatureName "Microsoft-Windows-Subsystem-Linux"
    if ($feature.State -ne "Enabled") {
        Write-Error "WSL2 is NOT enabled. Please run 'wsl --install' in an Admin prompt and restart."
        exit 1
    }
}
Write-Host "✅ WSL2 detected/enabled." -ForegroundColor Green

# 3. Check Docker Desktop
$docker = Get-Command docker -ErrorAction SilentlyContinue
if (-not $docker) {
    Write-Error "Docker Desktop not found in PATH. Please install from docker.com."
    exit 1
}
Write-Host "✅ Docker Desktop detected." -ForegroundColor Green

# 4. Check Git
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Error "Git not found. Please install from git-scm.com."
    exit 1
}
Write-Host "✅ Git detected." -ForegroundColor Green

# 5. Check gcloud SDK
$gcloud = Get-Command gcloud -ErrorAction SilentlyContinue
if (-not $gcloud) {
    Write-Warning "Google Cloud SDK not found. Cloud deployment will be disabled (Local Edge-only mode)."
} else {
    Write-Host "✅ Google Cloud SDK detected." -ForegroundColor Green
}

# 6. Check Hardware (Memory)
$mem = Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize
if ($mem.TotalVisibleMemorySize -lt 8000000) {
    Write-Warning "Device has less than 8GB RAM. Local inference performance may be degraded."
} else {
    Write-Host "✅ Hardware memory verified." -ForegroundColor Green
}

Write-Host "`n🌟 Pre-flight check complete. Your device is ready for Sovereign Deployment." -ForegroundColor Green
