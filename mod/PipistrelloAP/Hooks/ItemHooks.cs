using HarmonyLib;
using Pipistrello;

namespace PipistrelloAP.Hooks;

// SetEquipAcquired(Director director, Game.Equip equip, bool acquired, bool notify)
[HarmonyPatch(typeof(Game), nameof(Game.SetEquipAcquired))]
public static class SetEquipAcquiredPatch
{
    public static void Postfix(Game.Equip equip, bool acquired, bool __result)
    {
        if (!acquired || !__result) return;
        Plugin.Log.LogInfo($"[AP] EQUIP ACQUIRED: {equip?.name ?? "?"}");
    }
}

// SetUpgradeAcquired(Director director, Game.Upgrade upgrade, bool acquired)
[HarmonyPatch(typeof(Game), nameof(Game.SetUpgradeAcquired))]
public static class SetUpgradeAcquiredPatch
{
    public static void Postfix(Game.Upgrade upgrade, bool acquired, bool __result)
    {
        if (!acquired || !__result) return;
        Plugin.Log.LogInfo($"[AP] UPGRADE ACQUIRED: {upgrade?.name ?? "?"}");
    }
}

// SetPetalContainerAcquired(Director director, string id, int petalNum, bool acquired)
[HarmonyPatch(typeof(Game), nameof(Game.SetPetalContainerAcquired))]
public static class SetPetalContainerAcquiredPatch
{
    public static void Postfix(string id, int petalNum, bool acquired, bool __result)
    {
        if (!acquired || !__result) return;
        Plugin.Log.LogInfo($"[AP] PETAL CONTAINER ACQUIRED: {id}[{petalNum}]");
    }
}

// SetBpContainerAcquired(Director director, string id, int ..., bool acquired)
[HarmonyPatch(typeof(Game), nameof(Game.SetBpContainerAcquired))]
public static class SetBpContainerAcquiredPatch
{
    // Use positional args (__1, __2...) to avoid name mismatches
    public static void Postfix(string __1, bool __result)
    {
        if (!__result) return;
        Plugin.Log.LogInfo($"[AP] BP CONTAINER ACQUIRED: {__1}");
    }
}
