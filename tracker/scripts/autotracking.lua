-- autotracking.lua
-- Receives items and checks from Archipelago and updates the tracker state.

ITEM_MAPPING = {
    ["Yoyo"]          = "yoyo",
    ["Double Jump"]   = "double_jump",
    ["Dash"]          = "dash",
    ["Health Upgrade"] = "health_upgrade",
}

LOCATION_MAPPING = {
    [7371000] = "Starting Area - Tutorial Chest",
    [7371001] = "Cursed Forest - Chest 1",
    [7371500] = "Cursed Forest - Boss Reward",
}

function onArchipelagoConnected(slotData)
    print("[Pipistrello AP] Connected to Archipelago")
end

function onItemReceived(item)
    local name = item.item_name
    local code = ITEM_MAPPING[name]
    if not code then
        print("[Pipistrello AP] Unknown item: " .. tostring(name))
        return
    end

    local trackerItem = Tracker:FindObjectForCode(code)
    if not trackerItem then
        print("[Pipistrello AP] No tracker object for code: " .. code)
        return
    end

    if trackerItem.Type == "toggle" then
        trackerItem.Active = true
    elseif trackerItem.Type == "progressive" then
        trackerItem.CurrentStage = math.min(
            trackerItem.CurrentStage + 1,
            trackerItem.MaxStage
        )
    end

    print("[Pipistrello AP] Item received: " .. name)
end

function onLocationChecked(locationId)
    local name = LOCATION_MAPPING[locationId]
    if name then
        print("[Pipistrello AP] Location checked: " .. name)
    end
end

if Archipelago then
    Archipelago:OnConnected(onArchipelagoConnected)
    Archipelago:OnItemReceived(onItemReceived)
    Archipelago:OnLocationChecked(onLocationChecked)
end
