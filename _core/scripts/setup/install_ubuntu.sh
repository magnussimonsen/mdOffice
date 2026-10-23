#!/usr/bin/env bash

_mdoffice_is_sourced=false
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  _mdoffice_is_sourced=true
fi

_mdoffice_setup_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
_mdoffice_repo_root="$(cd -- "$_mdoffice_setup_dir/../../.." && pwd)"

_mdoffice_setup_ubuntu() {
  set -euo pipefail
  cd "$_mdoffice_repo_root"

  apt_has_package() {
    apt-cache show "$1" 2>/dev/null | grep -q "^Package: $1$"
  }

  echo "[mdOffice setup] Updating apt package lists..."
  sudo apt-get update

  local python_command=python3
  local python_packages=(python3 python3-venv)
  if apt_has_package python3.14 && apt_has_package python3.14-venv; then
    python_command=python3.14
    python_packages=(python3.14 python3.14-venv)
  elif command -v python3.14 >/dev/null 2>&1 && python3.14 -m venv --help >/dev/null 2>&1; then
    python_command=python3.14
    python_packages=()
  else
    echo "[mdOffice setup] Python 3.14 is not available from the configured Ubuntu sources; using the distro's python3."
  fi

  echo "[mdOffice setup] Installing Pandoc, LaTeX, and Python..."
  sudo apt-get install -y \
    pandoc \
    texlive-xetex \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-science \
    "${python_packages[@]}"

  echo "[mdOffice setup] Checking required LaTeX packages..."
  local package_list="_core/scripts/setup/latex-required-packages.txt"
  local package
  while IFS= read -r package; do
    [[ -z "$package" || "$package" == \#* ]] && continue
    if ! kpsewhich "${package}.sty" >/dev/null 2>&1; then
      echo "Required LaTeX package is missing: ${package}.sty" >&2
      return 1
    fi
  done < "$package_list"

  echo "[mdOffice setup] Creating virtual environment (.venv)..."
  if [[ -d .venv ]]; then
    echo "[mdOffice setup] .venv already exists; reusing it."
  else
    "$python_command" -m venv .venv
  fi

  echo "[mdOffice setup] Installing Python requirements..."
  ./.venv/bin/python -m pip install --upgrade pip
  ./.venv/bin/python -m pip install -r _core/scripts/requirements.txt

  if [[ -e .vscode/settings.json ]]; then
    echo "[mdOffice setup] Keeping existing .vscode/settings.json."
  else
    echo "[mdOffice setup] Creating VS Code settings..."
    mkdir -p .vscode
    cp _core/vscode-settings-templates/settings.linux_with_highlights.json .vscode/settings.json
  fi

  if command -v code >/dev/null 2>&1; then
    echo "[mdOffice setup] Installing mdOffice VS Code extension (right-click > mdOffice in .md files)..."
    local vsix
    vsix="$(mktemp -d)/mdoffice-insert.vsix"
    ./.venv/bin/python _core/vscode-extension/build-vsix.py "$vsix"
    code --install-extension "$vsix" --force
    rm -f "$vsix"
  else
    echo "[mdOffice setup] VS Code command 'code' not found on PATH. Skipping the extension; see _core/vscode-extension/mdoffice-insert/README.md."
  fi
}

if ( _mdoffice_setup_ubuntu ); then
  source "$_mdoffice_repo_root/.venv/bin/activate"
  unset -f _mdoffice_setup_ubuntu
  if [[ "$_mdoffice_is_sourced" == true ]]; then
    echo "[mdOffice setup] Done. .venv is active in this terminal."
    echo "[mdOffice setup] Restart VS Code if it was open during setup."
    unset _mdoffice_setup_dir _mdoffice_repo_root _mdoffice_is_sourced
  elif [[ -t 0 && -t 1 ]]; then
    echo "[mdOffice setup] Done. Starting an interactive shell with .venv active."
    echo "[mdOffice setup] Restart VS Code if it was open during setup."
    unset _mdoffice_setup_dir _mdoffice_repo_root _mdoffice_is_sourced
    exec "${SHELL:-/bin/bash}" -i
  else
    echo "[mdOffice setup] Done. Activate .venv with: source .venv/bin/activate"
    echo "[mdOffice setup] Restart VS Code if it was open during setup."
    unset _mdoffice_setup_dir _mdoffice_repo_root _mdoffice_is_sourced
  fi
else
  _mdoffice_status=$?
  unset -f _mdoffice_setup_ubuntu
  if [[ "$_mdoffice_is_sourced" == true ]]; then
    unset _mdoffice_setup_dir _mdoffice_repo_root _mdoffice_is_sourced
    return "$_mdoffice_status"
  else
    unset _mdoffice_setup_dir _mdoffice_repo_root _mdoffice_is_sourced
    exit "$_mdoffice_status"
  fi
fi
