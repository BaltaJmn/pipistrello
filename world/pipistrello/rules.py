from BaseClasses import CollectionState


def has(state: CollectionState, player: int, item: str) -> bool:
    return state.has(item, player)


def can_fight(state: CollectionState, player: int) -> bool:
    return has(state, player, "Yoyo")


def can_reach_high(state: CollectionState, player: int) -> bool:
    return has(state, player, "Double Jump")


def can_cross_gaps(state: CollectionState, player: int) -> bool:
    return has(state, player, "Dash")


def set_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

    # Region connection rules
    for entrance in multiworld.get_region("Starting Area", player).exits:
        if entrance.connected_region.name == "Cursed Forest":
            entrance.access_rule = lambda state: can_fight(state, player)

    for entrance in multiworld.get_region("Cursed Forest", player).exits:
        if entrance.connected_region.name == "Deep Forest":
            entrance.access_rule = lambda state: can_reach_high(state, player)

    # Location-specific rules
    forest_boss = multiworld.get_location("Cursed Forest - Boss Reward", player)
    forest_boss.access_rule = lambda state: can_fight(state, player)

    # Completion condition
    multiworld.completion_condition[player] = \
        lambda state: state.has("Victory", player)
