# Install mdOffice

1. Install Python 3.14 and Pandoc. To create PDFs, also install a LaTeX
   distribution that provides `xelatex`: MiKTeX on Windows, TeX Live on Linux,
   or MacTeX on macOS.
2. From the repository root, run the setup script for your system:

   **Windows (CMD or PowerShell):**
   ```bat
   _core\scripts\setup\install_windows.bat
   ```

   **Linux or macOS (bash):**
   ```bash
   bash _core/scripts/setup/install_linux.sh
   ```

   The script creates `.venv`, installs Python requirements, checks Pandoc and
   LaTeX, and configures VS Code.
3. In VS Code, install the recommended **Run on Save** extension,
   `emeraldwalk.runonsave`, and restart VS Code if it was already open.
4. Open and save a Markdown example in `_core/examples/`. Generated files are
   placed in a format-specific folder beside the Markdown file, such as `pdf/`.