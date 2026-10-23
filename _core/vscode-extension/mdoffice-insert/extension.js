// mdOffice Insert: inserts _core/quick-start/quickstart-<template>.md.
// In an empty file the whole template goes in (frontmatter and example content).
// In a file that already has text, only the frontmatter is inserted, at the
// cursor (right-clicking moves the cursor to where you click).
//
// New template in the menu:
//   1. Create _core/quick-start/quickstart-<template>.md (it shows up in "choose template" automatically).
//   2. For a dedicated menu item: add a command in package.json (commands + menus)
//      and a line in FIXED_COMMANDS below. Reload VS Code.
const vscode = require("vscode");
const fs = require("fs");
const path = require("path");

const FIXED_COMMANDS = {
  "mdoffice.insertStandardPdf": "quickstart-standard-pdf.md",
  "mdoffice.insertFancyPdf": "quickstart-fancy-pdf.md",
  "mdoffice.insertExamPdf": "quickstart-exam-pdf.md",
  "mdoffice.insertFancyBeamer": "quickstart-fancy-beamer.md",
};

function findQuickstartDir() {
  const configured = vscode.workspace.getConfiguration("mdofficeInsert").get("quickstartDir");
  const candidates = [];
  if (configured) candidates.push(configured);
  // Search upwards from the open file for _core/quick-start.
  const editor = vscode.window.activeTextEditor;
  if (editor && editor.document.uri.scheme === "file") {
    let dir = path.dirname(editor.document.uri.fsPath);
    while (true) {
      candidates.push(path.join(dir, "_core", "quick-start"));
      const parent = path.dirname(dir);
      if (parent === dir) break;
      dir = parent;
    }
  }
  // The extension lives in _core/vscode-extension/mdoffice-insert (via junction).
  candidates.push(path.resolve(fs.realpathSync(__dirname), "..", "..", "quick-start"));
  for (const f of vscode.workspace.workspaceFolders || []) {
    candidates.push(path.join(f.uri.fsPath, "_core", "quick-start"));
    candidates.push(path.join(f.uri.fsPath, "quick-start"));
  }
  return candidates.find((c) => fs.existsSync(c));
}

// Reads the whole template, or only the frontmatter block (from the first
// --- to the next ---), with the date set to today.
function readTemplate(file, frontmatterOnly) {
  const text = fs.readFileSync(file, "utf8").replace(/\r\n/g, "\n");
  const m = text.match(/^---\n[\s\S]*?\n---\n/);
  if (!m) throw new Error(`No frontmatter found in ${file}`);
  // Local date (toISOString gives UTC and can return yesterday's date around midnight).
  const d = new Date();
  const today = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  return (frontmatterOnly ? m[0] : text).replace(/^date: ".*"$/m, `date: "${today}"`);
}

async function insertFrom(fileName) {
  const editor = vscode.window.activeTextEditor;
  if (!editor) return;
  const dir = findQuickstartDir();
  if (!dir) {
    vscode.window.showErrorMessage("mdOffice: could not find _core/quick-start. Set mdofficeInsert.quickstartDir.");
    return;
  }
  const file = path.join(dir, fileName);
  const frontmatterOnly = editor.document.getText().trim() !== "";
  let block;
  try {
    block = readTemplate(file, frontmatterOnly);
  } catch (e) {
    vscode.window.showErrorMessage(`mdOffice: ${e.message}`);
    return;
  }
  const eol = editor.document.eol === vscode.EndOfLine.CRLF ? "\r\n" : "\n";
  block = block.replace(/\n/g, eol);
  const pos = editor.selection.active;
  // Add a line break first if the cursor is not at the start of the line.
  if (pos.character > 0) block = eol + block;
  await editor.edit((b) => b.insert(pos, block));
  if (frontmatterOnly) {
    vscode.window.setStatusBarMessage("mdOffice: the file already has text, so only the frontmatter was inserted. Use an empty file to get the full example.", 8000);
  }
}

async function pickAndInsert() {
  const dir = findQuickstartDir();
  if (!dir) {
    vscode.window.showErrorMessage("mdOffice: could not find _core/quick-start.");
    return;
  }
  const items = fs
    .readdirSync(dir)
    .filter((f) => /^quickstart-.*\.md$/.test(f))
    .map((f) => ({ label: f.replace(/^quickstart-|\.md$/g, ""), description: f, file: f }));
  const choice = await vscode.window.showQuickPick(items, { placeHolder: "Choose an mdOffice template" });
  if (choice) await insertFrom(choice.file);
}

function activate(context) {
  for (const [cmd, file] of Object.entries(FIXED_COMMANDS)) {
    context.subscriptions.push(vscode.commands.registerCommand(cmd, () => insertFrom(file)));
  }
  context.subscriptions.push(vscode.commands.registerCommand("mdoffice.insertPick", pickAndInsert));
}

function deactivate() {}

module.exports = { activate, deactivate };
