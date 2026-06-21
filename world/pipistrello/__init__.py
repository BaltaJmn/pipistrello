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
    item_name_to_id = {name: data.id for name, data in ITEM_TABLE.items()}
    location_name_to_id = {name: data.id for name, data in LOCATION_TABLE.items()}

    def create_item(self, name: str) -> PipistrelloItem:
        data = ITEM_TABLE[name]
        return PipistrelloItem(name, data.classification, data.id, self.player)

    def create_items(self) -> None:
        items_to_create = []
        for name, data in ITEM_TABLE.items():
            if data.classification == ItemClassification.event:
                continue
            for _ in range(data.count):
                items_to_create.append(self.create_item(name))

        # Pad with filler if location count exceeds item count
        loc_count = len(LOCATION_TABLE)
        while len(items_to_create) < loc_count:
            items_to_create.append(self.create_item("Gold Coin"))

        self.multiworld.itempool += items_to_create

    def create_regions(self) -> None:
        create_regions(self)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        victory = self.create_item("Victory")
        self.multiworld.get_location("Victory", self.player).place_locked_item(victory)
