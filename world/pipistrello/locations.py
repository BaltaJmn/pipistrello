import json
import pkgutil
from dataclasses import dataclass, field
from BaseClasses import Location


@dataclass
class LocationData:
    id: int
    region: str
    access_rules: list[str] = field(default_factory=list)


def _load_locations() -> dict[str, LocationData]:
    raw = json.loads(pkgutil.get_data(__package__, "_data/locations.json").decode("utf-8"))
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
