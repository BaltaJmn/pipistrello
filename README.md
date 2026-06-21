# Pipistrello and the Cursed Yoyo — Archipelago

Archipelago randomizer integration for *Pipistrello and the Cursed Yoyo*.

## Components

| Component | Path | Language |
|-----------|------|----------|
| APWorld | `world/pipistrello/` | Python 3.11 |
| BepInEx Mod | `mod/PipistrelloAP/` | C# (.NET 6) |
| PopTracker Pack | `tracker/` | Lua + JSON |
| Shared Data | `shared/data/` | JSON |

## Quick Start

### Prerequisites
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago) (for APWorld development)
- [BepInEx 6.x](https://github.com/BepInEx/BepInEx) (installed in game folder)
- [PopTracker](https://github.com/black-sliver/PopTracker) (for tracker development)
- Python 3.11+
- .NET 6 SDK

### Validate shared data
```bash
pip install jsonschema
python shared/scripts/validate.py
```

### Install APWorld
```bash
cp -r world/pipistrello <archipelago-folder>/worlds/
```

### Build mod
```bash
cd mod/PipistrelloAP
dotnet build
```

## Data

All items, locations and regions are defined once in `shared/data/` and consumed by every component.
Never duplicate these lists — edit them there and run `validate.py`.

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md).
