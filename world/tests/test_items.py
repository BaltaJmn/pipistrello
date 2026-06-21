from test import WorldTestBase


class TestPipistrelloBase(WorldTestBase):
    game = "Pipistrello and the Cursed Yoyo"


class TestAccessibility(TestPipistrelloBase):

    def test_starting_area_reachable_from_start(self):
        self.assertAccessDependency(
            ["Starting Area - Tutorial Chest"],
            [[]],
        )

    def test_forest_requires_yoyo(self):
        self.assertFalse(
            self.multiworld.get_location("Cursed Forest - Chest 1", self.player)
            .can_reach(self.multiworld.state)
        )

    def test_forest_accessible_with_yoyo(self):
        self.collect_by_name("Yoyo")
        self.assertTrue(
            self.multiworld.get_location("Cursed Forest - Chest 1", self.player)
            .can_reach(self.multiworld.state)
        )

    def test_boss_accessible_with_yoyo(self):
        self.collect_by_name("Yoyo")
        self.assertTrue(
            self.multiworld.get_location("Cursed Forest - Boss Reward", self.player)
            .can_reach(self.multiworld.state)
        )
