"""Packages mdoffice-insert into a .vsix without npm/vsce.
Usage:  python build-vsix.py [outfile.vsix]   and then   code --install-extension mdoffice-insert.vsix --force

The extension has the same version as mdOffice: the number in _core/VERSION
is copied into package.json before packaging.
"""
import json, re, sys, zipfile
from pathlib import Path

here = Path(__file__).resolve().parent
src = here / "mdoffice-insert"
version = (here.parent / "VERSION").read_text(encoding="utf-8").strip()
pkg_file = src / "package.json"
pkg_text = pkg_file.read_text(encoding="utf-8")
synced = re.sub(r'("version"\s*:\s*")[^"]*(")', rf"\g<1>{version}\g<2>", pkg_text, count=1)
if synced != pkg_text:
    pkg_file.write_text(synced, encoding="utf-8")
    print(f"package.json version set to {version}")
pkg = json.loads(synced)
out = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else here / "mdoffice-insert.vsix"

manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="{pkg['name']}" Version="{pkg['version']}" Publisher="{pkg['publisher']}"/>
    <DisplayName>{pkg['displayName']}</DisplayName>
    <Description xml:space="preserve">{pkg['description']}</Description>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="{pkg['engines']['vscode']}"/>
    </Properties>
  </Metadata>
  <Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
  <Dependencies/>
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true"/>
    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true"/>
    <Asset Type="Microsoft.VisualStudio.Services.Icons.Default" Path="extension/{pkg['icon']}" Addressable="true"/>
  </Assets>
</PackageManifest>
"""
content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension=".json" ContentType="application/json"/>
  <Default Extension=".js" ContentType="application/javascript"/>
  <Default Extension=".md" ContentType="text/markdown"/>
  <Default Extension=".png" ContentType="image/png"/>
  <Default Extension=".vsixmanifest" ContentType="text/xml"/>
</Types>
"""
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("extension.vsixmanifest", manifest)
    z.writestr("[Content_Types].xml", content_types)
    for f in src.iterdir():
        if f.is_file():
            z.write(f, f"extension/{f.name}")
print(f"Created {out}")
