# build_apworld.ps1
# Builds pipistrello.apworld and optionally installs it into an Archipelago installation.
#
# Usage:
#   .\tools\build_apworld.ps1
#   .\tools\build_apworld.ps1 -Install "C:\ProgramData\Archipelago"

param(
    [string]$Install = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$worldSrc = Join-Path $root "world\pipistrello"
$sharedData = Join-Path $root "shared\data"
$tmp = Join-Path $env:TEMP "apwbuild_pipistrello"
$outZip = Join-Path $env:TEMP "pipistrello.zip"
$outApworld = Join-Path $root "dist\pipistrello.apworld"

# 1. Sync _data/ from shared/data/
Write-Host "Syncing _data/ from shared/data/ ..."
$dataDir = Join-Path $worldSrc "_data"
New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
foreach ($f in @("items.json", "locations.json", "regions.json")) {
    Copy-Item (Join-Path $sharedData $f) (Join-Path $dataDir $f) -Force
}

# 2. Stage build in temp dir
Write-Host "Staging build ..."
if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
New-Item -ItemType Directory -Path "$tmp\pipistrello\_data" -Force | Out-Null

$pyFiles = @("__init__.py", "items.py", "locations.py", "options.py", "regions.py", "rules.py")
foreach ($f in $pyFiles) {
    Copy-Item (Join-Path $worldSrc $f) "$tmp\pipistrello\$f"
}
foreach ($f in @("items.json", "locations.json", "regions.json")) {
    Copy-Item (Join-Path $dataDir $f) "$tmp\pipistrello\_data\$f"
}

# archipelago.json manifest (required for AP 0.7.0+)
[System.IO.File]::WriteAllText("$tmp\archipelago.json",
    '{"game": "Pipistrello and the Cursed Yoyo", "version": "0.1.0"}')

# 3. Pack into ZIP then rename to .apworld
Write-Host "Packing ..."
New-Item -ItemType Directory -Path (Split-Path $outApworld) -Force | Out-Null
if (Test-Path $outZip) { [System.IO.File]::Delete($outZip) }
if (Test-Path $outApworld) { [System.IO.File]::Delete($outApworld) }

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory(
    $tmp, $outZip,
    [System.IO.Compression.CompressionLevel]::Optimal, $false)
[System.IO.File]::Move($outZip, $outApworld)

$kb = [math]::Round((Get-Item $outApworld).Length / 1KB, 1)
Write-Host "Built: $outApworld ($kb KB)"

# 4. Optional install
if ($Install -ne "") {
    $dest = Join-Path $Install "custom_worlds\pipistrello.apworld"
    Copy-Item $outApworld $dest -Force
    Write-Host "Installed: $dest"
}

Write-Host "Done."
