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

        LocationManager.OnFlagSet(flag);

        // Abilities are AP items (received from AP, not sent as checks) — log separately
        // TODO Phase 3: route to ItemManager.OnAbilityGranted(flag) instead
        if (flag.StartsWith("g:ability:"))
            Plugin.Log.LogInfo($"[AP] ABILITY: {flag}");
    }
}
