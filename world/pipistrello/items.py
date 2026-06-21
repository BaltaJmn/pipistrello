import json
from dataclasses import dataclass
from pathlib import Path
from BaseClasses import ItemClassification, Item

_SHARED_DATA = Path(__file__).parent.parent.parent / "shared" / "data" / "items.json"

_CLASSIFICATION_MAP = {
    "progression": ItemClassification.progression,
    "useful":      ItemClassification.useful,
    "filler":      ItemClassification.filler,
    "trap":        ItemClassification.trap,
    "event":       ItemClassification.progression,
}


@dataclass
class ItemData:
    id: int
    classification: ItemClassification
    count: int


def _load_items() -> dict[str, ItemData]:
    with open(_SHARED_DATA, encoding="utf-8") as f:
        raw = json.load(f)
    return {
        item["name"]: ItemData(
            id=item["id"],
            classification=_CLASSIFICATION_MAP[item["classification"]],
            count=item.get("count", 1),
        )
        for item in raw["items"]
    }


ITEM_TABLE: dict[str, ItemData] = _load_items()

# Victory event — not in shared/data, internal to APWorld only
ITEM_TABLE["Victory"] = ItemData(
    id=None,
    classification=ItemClassification.progression,
    count=1,
)


class PipistrelloItem(Item):
    game = "Pipistrello and the Cursed Yoyo"
