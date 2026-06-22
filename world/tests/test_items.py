from test import WorldTestBase


class TestPipistrelloBase(WorldTestBase):
    game = "Pipistrello and the Cursed Yoyo"


class TestGeneration(TestPipistrelloBase):

    def test_all_locations_created(self):
        location_names = [loc.name for loc in self.multiworld.get_locations(self.player)]
        expected = [
            "Police Department - Boss Cleared",
            "Police Department - Vision Sensor",
            "Police Department - BP Upgrade",
            "City Interiors - Petal Container 1",
            "City Interiors - Petal Container 2",
            "Tunnels - Battery 1",
            "Tunnels - Battery 2",
        ]
        for name in expected:
            self.assertIn(name, location_names, f"Missing location: {name}")

    def test_all_progression_items_in_pool(self):
        item_names = [item.name for item in self.multiworld.itempool]
        for ability in ["Throw", "Wall Dash", "Walk The Dog", "Wall Railing", "Helix"]:
            self.assertIn(ability, item_names, f"Missing progression item: {ability}")

    def test_item_count_matches_location_count(self):
        item_count = len(self.multiworld.itempool)
        loc_count = len([
            loc for loc in self.multiworld.get_locations(self.player)
            if loc.item is None  # exclude pre-placed event items
        ])
        self.assertEqual(item_count, loc_count,
                         f"Item pool ({item_count}) must equal non-event location count ({loc_count})")


class TestAccessibility(TestPipistrelloBase):

    def test_all_locations_reachable_from_start(self):
        """Phase 2 stub: no access rules, everything reachable immediately."""
        state = self.multiworld.get_all_state(False)
        for loc in self.multiworld.get_locations(self.player):
            if loc.name == "Victory":
                continue
            self.assertTrue(
                loc.can_reach(state),
                f"Location '{loc.name}' should be reachable from start in Phase 2 stub"
            )

    def test_completion_requires_all_abilities(self):
        state = self.multiworld.get_all_state(False)
        self.assertFalse(
            self.multiworld.completion_condition[self.player](state),
            "Should not be complete with empty state"
        )
        for ability in ["Throw", "Wall Dash", "Walk The Dog", "Wall Railing", "Helix"]:
            self.collect_by_name(ability)
        self.assertTrue(
            self.multiworld.completion_condition[self.player](self.multiworld.state),
            "Should be complete with all progression abilities"
        )
