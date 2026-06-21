import json
from pathlib import Path
from BaseClasses import Region
from .locations import LOCATION_TABLE, PipistrelloLocation

_SHARED_DATA = Path(__file__).parent.parent.parent / "shared" / "data" / "regions.json"


def create_regions(world) -> None:
    player = world.player
    multiworld = world.multiworld

    with open(_SHARED_DATA, encoding="utf-8") as f:
        raw = json.load(f)

    region_map: dict[str, Region] = {}

    # Create region objects
    for r in raw["regions"]:
        region = Region(r["name"], player, multiworld)
        region_map[r["id"]] = region

    # Add Menu if not in data (required by AP)
    if "menu" not in region_map:
        region_map["menu"] = Region("Menu", player, multiworld)

    # Place locations into their regions
    for loc_name, loc_data in LOCATION_TABLE.items():
        region_id = loc_data.region
        if region_id not in region_map:
            raise ValueError(f"Location '{loc_name}' references unknown region '{region_id}'")
        region = region_map[region_id]
        location = PipistrelloLocation(player, loc_name, loc_data.id, region)
        region.locations.append(location)

    # Wire up connections (rules applied later in rules.py)
    for r in raw["regions"]:
        source = region_map[r["id"]]
        for conn in r.get("connects_to", []):
            target = region_map[conn["target"]]
            source.connect(target)

    # Connect Menu to starting_area if not already wired
    menu = region_map["menu"]
    if not any(e.connected_region == region_map.get("starting_area") for e in menu.exits):
        menu.connect(region_map["starting_area"])

    multiworld.regions += list(region_map.values())
