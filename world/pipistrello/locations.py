import json
from dataclasses import dataclass, field
from pathlib import Path
from BaseClasses import Location

_SHARED_DATA = Path(__file__).parent.parent.parent / "shared" / "data" / "locations.json"


@dataclass
class LocationData:
    id: int
    region: str
    access_rules: list[str] = field(default_factory=list)


def _load_locations() -> dict[str, LocationData]:
    with open(_SHARED_DATA, encoding="utf-8") as f:
        raw = json.load(f)
    return {
        loc["name"]: LocationData(
            id=loc["id"],
            region=loc["region"],
            access_rules=loc.get("access_rules", []),
        )
        for loc in raw["locations"]
    }


LOCATION_TABLE: dict[str, LocationData] = _load_locations()

# Victory — internal event location, placed in police_dep (Phase 2 stub; update region in Phase 4)
LOCATION_TABLE["Victory"] = LocationData(id=None, region="police_dep")


class PipistrelloLocation(Location):
    game = "Pipistrello and the Cursed Yoyo"
