from BaseClasses import CollectionState


def has(state: CollectionState, player: int, item: str) -> bool:
    return state.has(item, player)


# ── Access helpers (Phase 4: fill these in with real logic) ─────────────────

def can_wall_traverse(state: CollectionState, player: int) -> bool:
    return has(state, player, "Wall Dash") or has(state, player, "Wall Railing")


def can_reach_high(state: CollectionState, player: int) -> bool:
    return has(state, player, "Helix")


# ── Rule wiring ─────────────────────────────────────────────────────────────

def set_rules(world) -> None:
    player = world.player
    multiworld = world.multiworld

    # Phase 2 stub: no location or region rules — everything accessible from start.
    # Real access logic goes here in Phase 4 once the full map is catalogued.

    # Completion condition: have all 5 progression abilities
    # (Phase 4: replace with actual final boss condition)
    multiworld.completion_condition[player] = lambda state: (
        has(state, player, "Throw") and
        has(state, player, "Wall Dash") and
        has(state, player, "Walk The Dog") and
        has(state, player, "Wall Railing") and
        has(state, player, "Helix")
    )
