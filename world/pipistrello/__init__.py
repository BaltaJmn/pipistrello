from worlds.AutoWorld import World
from BaseClasses import ItemClassification, Item, Location
from .items import PipistrelloItem, ITEM_TABLE
from .locations import PipistrelloLocation, LOCATION_TABLE
from .regions import create_regions
from .rules import set_rules
from .options import PipistrelloOptions


class PipistrelloWorld(World):
    """Pipistrello and the Cursed Yoyo randomizer."""

    game = "Pipistrello and the Cursed Yoyo"
    options_dataclass = PipistrelloOptions
    item_name_to_id = {name: data.id for name, data in ITEM_TABLE.items() if data.id is not None}
    location_name_to_id = {name: data.id for name, data in LOCATION_TABLE.items() if data.id is not None}

    def create_item(self, name: str) -> PipistrelloItem:
        data = ITEM_TABLE[name]
        return PipistrelloItem(name, data.classification, data.id, self.player)

    def create_items(self) -> None:
        items_to_create = []
        for name, data in ITEM_TABLE.items():
            if data.id is None:  # event items (Victory) have no AP ID
                continue
            for _ in range(data.count):
                items_to_create.append(self.create_item(name))

        # Pad with filler to match fillable locations (exclude event locations with id=None)
        fillable = sum(1 for d in LOCATION_TABLE.values() if d.id is not None)
        while len(items_to_create) < fillable:
            items_to_create.append(self.create_item("Gold Coin"))

        self.multiworld.itempool += items_to_create

    def create_regions(self) -> None:
        create_regions(self)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        victory = self.create_item("Victory")
        self.multiworld.get_location("Victory", self.player).place_locked_item(victory)
