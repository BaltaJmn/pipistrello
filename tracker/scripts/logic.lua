-- logic.lua
-- Accessibility helper functions, called by PopTracker when evaluating access_rules.

function has(code)
    local item = Tracker:FindObjectForCode(code)
    return item ~= nil and item.Active
end

function can_fight()
    return has("yoyo")
end

function can_reach_high()
    return has("double_jump")
end

function can_cross_gaps()
    return has("dash")
end
