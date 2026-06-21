namespace PipistrelloAP;

public static class LocationManager
{
    // flag name → AP location ID
    // IDs in range 7371000–7372999
    // Add entries here as new locations are catalogued in shared/data/locations.json
    static readonly Dictionary<string, long> Table = new()
    {
        // --- Police Department ---
        ["g:policedepComplete"]                                     = 7371000,
        ["g:equip:seeEnemyLife:acquired"]                          = 7371001,
        ["g:upgrade:bpUp:acquired"]                                = 7371002,

        // --- City Interiors ---
        ["g:petalContainer:city_interiors/ren24/ren66:acquired"]   = 7371010,
        ["g:petalContainer:city_interiors/ren925/yug711:acquired"] = 7371011,

        // --- Tunnels ---
        ["g:tunnels:gotBattery1"]                                  = 7371020,
        ["g:tunnels:gotBattery2"]                                  = 7371021,
    };

    // Tracks flags already sent this session — prevents duplicate checks on save-load replay
    static readonly HashSet<string> Sent = new HashSet<string>();

    // Call when starting a new AP session (not needed on death/respawn — Sent intentionally persists)
    public static void Reset() => Sent.Clear();

    public static void OnFlagSet(string flag)
    {
        if (!IsLocationFlag(flag)) return;

        if (!Table.TryGetValue(flag, out var locationId))
        {
            // Flag matches a location pattern but isn't in the table yet — log for cataloguing
            Plugin.Log.LogInfo($"[AP] UNCATALOGUED: {flag}");
            return;
        }

        if (!Sent.Add(flag)) return; // already sent this session

        Plugin.Log.LogInfo($"[AP] CHECK: {flag} → {locationId}");
        // TODO Phase 2: ArchipelagoClient.SendLocationCheck(locationId);
    }

    // Returns true for flag patterns that represent collectible locations.
    // g:ability:* is intentionally excluded — abilities are AP items, not location checks.
    static bool IsLocationFlag(string f) =>
        (f.StartsWith("g:equip:") && f.EndsWith(":acquired")) ||
        (f.StartsWith("g:upgrade:") && f.EndsWith(":acquired")) ||
        (f.StartsWith("g:petalContainer:") && f.EndsWith(":acquired")) ||
        f.StartsWith("g:tunnels:gotBattery") ||
        (f.StartsWith("g:") && f.EndsWith("Complete"));
}
