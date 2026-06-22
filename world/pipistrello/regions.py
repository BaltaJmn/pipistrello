import json
import pkgutil
from BaseClasses import Region
from .locations import LOCATION_TABLE, PipistrelloLocation


def create_regions(world) -> None:
    player = world.player
    multiworld = world.multiworld

    raw = json.loads(pkgutil.get_data(__package__, "_data/regions.json").decode("utf-8"))

    region_map: dict[str, Region] = {}

    # Create region objects
    for r in raw["regions"]:
        region = Region(r["name"], player, multiworld)
        region_map[r["id"]] = region

    # AP requires a "Menu" region as the starting point
    if "menu" not in region_map:
        menu = Region("Menu", player, multiworld)
        region_map["menu"] = menu
        # Connect to first non-menu region if menu has no connections in data
        first = next((r for r in raw["regions"] if r["id"] != "menu"), None)
        if first:
            menu.connect(region_map[first["id"]])

    # Place locations into their regions
    for loc_name, loc_data in LOCATION_TABLE.items():
        region_id = loc_data.region
        if region_id not in region_map:
            raise ValueError(f"Location '{loc_name}' references unknown region '{region_id}'")
        region = region_map[region_id]
        location = PipistrelloLocation(player, loc_name, loc_data.id, region)
        region.locations.append(location)

    # Wire up connections between regions (access rules applied later in rules.py)
    for r in raw["regions"]:
        source = region_map[r["id"]]
        for conn in r.get("connects_to", []):
            target_id = conn["target"]
            if target_id not in region_map:
                raise ValueError(f"Region '{r['id']}' connects to unknown region '{target_id}'")
            source.connect(region_map[target_id])

    multiworld.regions += list(region_map.values())
