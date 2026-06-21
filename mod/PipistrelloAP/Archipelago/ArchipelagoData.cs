namespace PipistrelloAP.Archipelago;

/// <summary>
/// Stores connection details and session state for an AP multiworld run.
/// Persists across the game session so items received offline can be resynced on reconnect.
/// </summary>
public class ArchipelagoData
{
    public string Uri = "localhost";
    public string SlotName = "Player1";
    public string? Password;

    /// <summary>AP item index — tracks how many received items we've already processed.</summary>
    public int Index;

    /// <summary>Location IDs sent this session. Used to resync with the server on reconnect.</summary>
    public List<long> CheckedLocations = new();

    public string? Seed;

    public ArchipelagoData() { }

    public ArchipelagoData(string uri, string slotName, string? password)
    {
        Uri = uri;
        SlotName = slotName;
        Password = password;
    }

    public void SetupSession(Dictionary<string, object> slotData, string seed)
    {
        Seed = seed;
        // slotData can carry game-specific settings from the APWorld — parse here in Phase 4
    }
}
