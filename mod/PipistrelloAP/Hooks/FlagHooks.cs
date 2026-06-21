using HarmonyLib;
using Pipistrello;
using Il2CppDict = Il2CppSystem.Collections.Generic.Dictionary<string, int>;

namespace PipistrelloAP.Hooks;

// SetFlag(Dictionary<string,int> flags, string flagName, ...)
// __0 = the flag dictionary, __1 = flag name string
[HarmonyPatch(typeof(Game), nameof(Game.SetFlag))]
public static class SetFlagPatch
{
    public static void Postfix(Il2CppDict __0, string __1)
    {
        var flag = __1 ?? "";

        // AP-relevant flags only
        if (flag.StartsWith("g:equip:") && flag.EndsWith(":acquired"))
            Plugin.Log.LogInfo($"[AP] EQUIP ACQUIRED: {flag}");
        else if (flag.StartsWith("g:upgrade:") && flag.EndsWith(":acquired"))
            Plugin.Log.LogInfo($"[AP] UPGRADE ACQUIRED: {flag}");
        else if (flag.StartsWith("g:petalContainer:") && flag.EndsWith(":acquired"))
            Plugin.Log.LogInfo($"[AP] PETAL ACQUIRED: {flag}");
        else if (flag.StartsWith("g:tunnels:gotBattery"))
            Plugin.Log.LogInfo($"[AP] BATTERY: {flag}");
        else if (flag.EndsWith("Complete"))
            Plugin.Log.LogInfo($"[AP] AREA COMPLETE: {flag}");
        else if (flag.StartsWith("g:ability:"))
            Plugin.Log.LogInfo($"[AP] ABILITY: {flag}");
    }
}
