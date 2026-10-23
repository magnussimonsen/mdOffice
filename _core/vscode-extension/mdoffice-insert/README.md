# mdOffice Insert (local VS Code extension)

Right-click in a Markdown file and choose **mdOffice**. The menu items insert a template from `_core/quick-start/quickstart-*.md`. The date is set to today's date.

- **In an empty file**, the whole template is inserted: the frontmatter and a short example document. The example shows the syntax for that theme, with explanations in comments, and builds into a sample PDF the first time you save.
- **In a file that already has text**, only the frontmatter is inserted, at the cursor position.

- **Insert mdOffice standard-pdf template** uses `quickstart-standard-pdf.md`.
- **Insert mdOffice fancy-pdf template** uses `quickstart-fancy-pdf.md`.
- **Insert mdOffice exam-pdf template** uses `quickstart-exam-pdf.md`.
- **Insert mdOffice fancy-beamer template** uses `quickstart-fancy-beamer.md`.
- **Insert mdOffice template (choose)...** lists every `quickstart-*.md` automatically.

The templates are read from the quickstart files every time. If you change a quickstart file, what the menu inserts changes too. The extension finds `_core/quick-start` by searching upwards from the Markdown file you have open.

## Installing

The install scripts in `_core/scripts/setup/` install the extension automatically, as long as the `code` command is on `PATH`. Reload VS Code afterwards.

Manually, from the mdOffice folder:

```bash
python _core/vscode-extension/build-vsix.py
code --install-extension _core/vscode-extension/mdoffice-insert.vsix --force
```

If you change `extension.js` or `package.json`, you must install again. Changes to the quickstart files do not need a new install.

For development on Windows you can create a link (junction) instead, so code changes take effect after **Developer: Reload Window**:

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.vscode\extensions\local.mdoffice-insert-2.1.0" -Target "<path to mdOffice>\_core\vscode-extension\mdoffice-insert"
```

The number in the folder name is the mdOffice version from `_core/VERSION`. The extension always has the same version as mdOffice: `build-vsix.py` copies it into `package.json`.

## Adding a menu item for a theme

1. Make sure `_core/quick-start/quickstart-<theme>.md` exists.
2. In `package.json`: add the command under `commands`, `menus.mdoffice.submenu` and `menus.commandPalette`.
3. In `extension.js`: add the command and file name to `FIXED_COMMANDS`.
4. Run **Developer: Reload Window**.
