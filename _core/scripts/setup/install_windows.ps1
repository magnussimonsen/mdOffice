param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# If your Python launcher is different, update this constant.
# Examples:
#   @("py", "-3.14")
#   @("python")
#   @("C:\\Path\\To\\python.exe")
$PythonCommand = @("py", "-3.14")

function Write-Step {
    param([string]$Message)
    Write-Host "[mdOffice setup] $Message" -ForegroundColor Cyan
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-Python {
    param([string[]]$Args)
    & $PythonCommand[0] @($PythonCommand[1..($PythonCommand.Length - 1)]) @Args
}

Write-Step "Checking Python..."
try {
    if ($PythonCommand.Length -gt 1) {
        & $PythonCommand[0] @($PythonCommand[1..($PythonCommand.Length - 1)]) --version | Out-Null
    }
    else {
        & $PythonCommand[0] --version | Out-Null
    }
}
catch {
    Write-Error @"
Python was not found with the configured command:
  $($PythonCommand -join ' ')

Install Python 3.14 first, or edit $PythonCommand in this script to your local Python alias/path.
"@
}

Write-Step "Checking pandoc..."
if (-not (Test-Command "pandoc")) {
    Write-Error "Pandoc is not installed or not on PATH. Install Pandoc and run this script again."
}

Write-Step "Checking xelatex (LaTeX)..."
if (-not (Test-Command "xelatex")) {
    Write-Error "xelatex is not installed or not on PATH. Install MiKTeX/TeX Live and run this script again."
}

Write-Step "Checking required LaTeX packages..."
$latexPackageListFile = "_core/scripts/setup/latex-required-packages.txt"
if (-not (Test-Path $latexPackageListFile)) {
    Write-Error "Missing package list file: $latexPackageListFile"
}
if (-not (Test-Command "kpsewhich")) {
    Write-Error "kpsewhich was not found on PATH. Ensure your LaTeX distribution is correctly installed and available on PATH."
}

$latexPackages = Get-Content $latexPackageListFile |
    ForEach-Object { $_.Trim() } |
    Where-Object { $_ -and -not $_.StartsWith("#") }

$missingLatexPackages = @()
foreach ($pkg in $latexPackages) {
    & kpsewhich "$pkg.sty" | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $missingLatexPackages += $pkg
    }
}

if ($missingLatexPackages.Count -gt 0) {
    Write-Error @"
Missing required LaTeX packages:
  $($missingLatexPackages -join ", ")

Install missing packages in MiKTeX/TeX Live and run this script again.
"@
}

Write-Step "Creating virtual environment (.venv)..."
if (Test-Path ".venv") {
    Write-Step ".venv already exists, reusing it."
}
else {
    if ($PythonCommand.Length -gt 1) {
        & $PythonCommand[0] @($PythonCommand[1..($PythonCommand.Length - 1)]) -m venv .venv
    }
    else {
        & $PythonCommand[0] -m venv .venv
    }
}

Write-Step "Installing Python requirements..."
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r "_core/scripts/requirements.txt"

Write-Step "Writing VS Code settings with highlight rules..."
$template = "_core/vscode-settings-templates/settings.windows_with_highlights.json"
$targetDir = ".vscode"
$targetFile = Join-Path $targetDir "settings.json"

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

if ((Test-Path $targetFile) -and (-not $Force)) {
    Write-Error "Found existing .vscode/settings.json. Re-run with -Force to overwrite it."
}

Copy-Item -Path $template -Destination $targetFile -Force

Write-Step "Done. mdOffice setup completed successfully."
Write-Host "Next: restart VS Code if it was open during tool installation." -ForegroundColor Green
