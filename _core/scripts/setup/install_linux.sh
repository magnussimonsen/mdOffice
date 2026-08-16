#!/usr/bin/env bash
set -euo pipefail

# Ubuntu dependency install (run from terminal before this script if needed):
#   sudo apt update
#   sudo apt install -y pandoc texlive-xetex texlive-fonts-extra
#   # fontawesome5.sty is provided by texlive-fonts-extra (not a package named fontawesome5)
#   kpsewhich fontawesome5.sty
#
# If texlive-fonts-extra fails to download (mirror/network hiccup), retry with:
#   sudo apt clean
#   sudo apt update
#   sudo apt -o Acquire::Retries=8 -o Acquire::http::Timeout=30 install --fix-missing texlive-fonts-extra
#
# If your local mirror keeps failing, switch to the main Ubuntu archive:
#   sudo sed -i 's|http://no.archive.ubuntu.com/ubuntu|http://archive.ubuntu.com/ubuntu|g' /etc/apt/sources.list
#   sudo apt update
#   sudo apt -o Acquire::Retries=8 install --fix-missing texlive-fonts-extra
#
# Python used by this script defaults to 3.14.
# If Python 3.14 is available on your system:
#   sudo apt install -y python3.14 python3.14-venv
# If it is not available, install your distro Python and update PYTHON_CMD below:
#   sudo apt install -y python3 python3-venv

# If your Python executable name is different, update this array.
# Examples:
#   PYTHON_CMD=(python3.14)
#   PYTHON_CMD=(python3)
#   PYTHON_CMD=(/opt/python/3.14/bin/python3.14)
PYTHON_CMD=(python3.14)

step() {
  echo "[mdOffice setup] $1"
}

check_cmd() {
  command -v "$1" >/dev/null 2>&1
}

step "Checking Python..."
if ! "${PYTHON_CMD[@]}" --version >/dev/null 2>&1; then
  cat <<'EOF'
Python was not found with the configured command.
Install Python 3.14 first, or edit PYTHON_CMD in this script to your local Python alias/path.
EOF
  exit 1
fi

step "Checking pandoc..."
if ! check_cmd pandoc; then
  echo "Pandoc is not installed or not on PATH. Install Pandoc and run this script again."
  exit 1
fi

step "Checking xelatex (LaTeX)..."
if ! check_cmd xelatex; then
  echo "xelatex is not installed or not on PATH. Install TeX Live/MacTeX and run this script again."
  exit 1
fi

step "Checking required LaTeX packages..."
LATEX_PACKAGE_LIST="_core/scripts/setup/latex-required-packages.txt"
if [[ ! -f "$LATEX_PACKAGE_LIST" ]]; then
  echo "Missing package list file: $LATEX_PACKAGE_LIST"
  exit 1
fi
if ! check_cmd kpsewhich; then
  echo "kpsewhich is not on PATH. Ensure your LaTeX distribution is correctly installed and available on PATH."
  exit 1
fi

mapfile -t LATEX_PACKAGES < <(grep -v '^#' "$LATEX_PACKAGE_LIST" | sed '/^\s*$/d')
MISSING_PACKAGES=()
for pkg in "${LATEX_PACKAGES[@]}"; do
  if ! kpsewhich "${pkg}.sty" >/dev/null 2>&1; then
    MISSING_PACKAGES+=("$pkg")
  fi
done

if (( ${#MISSING_PACKAGES[@]} > 0 )); then
  echo "Missing required LaTeX packages: ${MISSING_PACKAGES[*]}"
  echo "Install missing packages in TeX Live/MacTeX and run this script again."
  exit 1
fi

step "Creating virtual environment (.venv)..."
if [[ -d .venv ]]; then
  step ".venv already exists, reusing it."
else
  "${PYTHON_CMD[@]}" -m venv .venv
fi

# If pip is missing in an existing venv, repair with:
#   .venv/bin/python -m ensurepip --upgrade
#   .venv/bin/python -m pip install --upgrade pip setuptools wheel
# If repair fails, recreate the venv:
#   rm -rf .venv
#   bash _core/scripts/setup/install_linux.sh

step "Installing Python requirements..."
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r _core/scripts/requirements.txt

step "Writing VS Code settings with highlight rules..."
mkdir -p .vscode
if [[ -f .vscode/settings.json ]]; then
  echo "Found existing .vscode/settings.json. Remove it first if you want this script to replace it."
  exit 1
fi
cp _core/vscode-settings-templates/settings.linux_with_highlights.json .vscode/settings.json

step "Done. mdOffice setup completed successfully."
echo "Next: restart VS Code if it was open during tool installation."
