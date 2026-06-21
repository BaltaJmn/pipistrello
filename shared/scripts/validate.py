"""
Validates consistency across shared/data/ JSON files.
Run from repo root: python shared/scripts/validate.py
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("ERROR: Missing dependency. Run: pip install jsonschema")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"


def load(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_unique_ids(entries: list, field: str, label: str) -> None:
    ids = [e[field] for e in entries]
    seen, dupes = set(), set()
    for i in ids:
        (dupes if i in seen else seen).add(i)
    if dupes:
        print(f"  ERROR: Duplicate {field} in {label}: {sorted(dupes)}")
        sys.exit(1)


def check_location_regions(locations: list, region_ids: set) -> None:
    for loc in locations:
        if loc["region"] not in region_ids:
            print(f"  ERROR: Location '{loc['name']}' references unknown region '{loc['region']}'")
            sys.exit(1)


def check_region_connections(regions: list, region_ids: set) -> None:
    for region in regions:
        for conn in region.get("connects_to", []):
            if conn["target"] not in region_ids:
                print(f"  ERROR: Region '{region['id']}' connects to unknown region '{conn['target']}'")
                sys.exit(1)


def check_id_ranges(items: list, locations: list) -> None:
    warnings = []
    for item in items:
        if not (7370000 <= item["id"] <= 7370999):
            warnings.append(f"  WARN: Item '{item['name']}' ID {item['id']} outside expected range 7370000-7370999")
    for loc in locations:
        if not (7371000 <= loc["id"] <= 7372999):
            warnings.append(f"  WARN: Location '{loc['name']}' ID {loc['id']} outside expected range 7371000-7372999")
    for w in warnings:
        print(w)


def check_placeholder_fields(items: list, locations: list) -> None:
    """Warn about fields still containing PLACEHOLDER_ values."""
    count = 0
    for item in items:
        for field in ("mod_internal_name",):
            v = item.get(field, "")
            if isinstance(v, str) and v.startswith("PLACEHOLDER_"):
                print(f"  WARN: Item '{item['name']}' has placeholder {field}: {v}")
                count += 1
    for loc in locations:
        for field in ("mod_scene", "mod_object_path", "mod_flag"):
            v = loc.get(field, "")
            if isinstance(v, str) and v.startswith("PLACEHOLDER_"):
                count += 1
    if count:
        print(f"  WARN: {count} placeholder field(s) found — replace after game analysis")


def main() -> None:
    errors = False

    print("Loading data files...")
    items_data     = load(DATA / "items.json")
    locations_data = load(DATA / "locations.json")
    regions_data   = load(DATA / "regions.json")

    print("Validating schemas...")
    try:
        validate(items_data,     load(SCHEMAS / "item.schema.json"))
        validate(locations_data, load(SCHEMAS / "location.schema.json"))
        print("  OK: schemas valid")
    except ValidationError as e:
        print(f"  ERROR: Schema validation failed: {e.message}")
        sys.exit(1)

    print("Checking unique IDs...")
    check_unique_ids(items_data["items"],         "id", "items")
    check_unique_ids(locations_data["locations"], "id", "locations")
    print("  OK: no duplicate IDs")

    print("Checking region references...")
    region_ids = {r["id"] for r in regions_data["regions"]}
    check_location_regions(locations_data["locations"], region_ids)
    check_region_connections(regions_data["regions"], region_ids)
    print("  OK: all region references valid")

    print("Checking ID ranges...")
    check_id_ranges(items_data["items"], locations_data["locations"])

    print("Checking for placeholders...")
    check_placeholder_fields(items_data["items"], locations_data["locations"])

    item_count = sum(i.get("count", 1) for i in items_data["items"])
    loc_count  = len(locations_data["locations"])
    print(f"\nSummary: {len(items_data['items'])} item types ({item_count} total) | {loc_count} locations | {len(regions_data['regions'])} regions")

    if not errors:
        print("\n✓ All validations passed")


if __name__ == "__main__":
    main()
