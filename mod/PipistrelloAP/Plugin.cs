using BepInEx;
using BepInEx.Configuration;
using BepInEx.Unity.IL2CPP;
using BepInEx.Logging;
using HarmonyLib;
using PipistrelloAP.Archipelago;

namespace PipistrelloAP;

[BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
public class Plugin : BasePlugin
{
    internal static new ManualLogSource Log = null!;

    // Written to BepInEx/config/PipistrelloAP.cfg on first run
    static ConfigEntry<string> cfgHost = null!;
    static ConfigEntry<int>    cfgPort = null!;
    static ConfigEntry<string> cfgSlot = null!;
    static ConfigEntry<string> cfgPass = null!;

    public override void Load()
    {
        Log = base.Log;
        Log.LogInfo("=== PipistrelloAP loading ===");

        BindConfig();

        var harmony = new Harmony(MyPluginInfo.PLUGIN_GUID);
        harmony.PatchAll();

        InitArchipelago();

        Log.LogInfo("=== PipistrelloAP ready ===");
    }

    void BindConfig()
    {
        cfgHost = Config.Bind("Connection", "Host",     "localhost", "Archipelago server host");
        cfgPort = Config.Bind("Connection", "Port",     38281,       "Archipelago server port");
        cfgSlot = Config.Bind("Connection", "SlotName", "Player1",   "Your slot name in the multiworld");
        cfgPass = Config.Bind("Connection", "Password", "",          "Server password (leave empty if none)");
    }

    void InitArchipelago()
    {
        // Build URI — only append port if non-default, the AP client accepts "host:port" strings
        var host = cfgPort.Value == 38281
            ? cfgHost.Value
            : $"{cfgHost.Value}:{cfgPort.Value}";

        ArchipelagoClient.ServerData.Uri      = host;
        ArchipelagoClient.ServerData.SlotName = cfgSlot.Value;
        ArchipelagoClient.ServerData.Password = string.IsNullOrWhiteSpace(cfgPass.Value)
            ? null
            : cfgPass.Value;

        Log.LogInfo($"[AP] Connecting to {host} as '{cfgSlot.Value}'...");
        ArchipelagoClient.Connect();
    }
}
