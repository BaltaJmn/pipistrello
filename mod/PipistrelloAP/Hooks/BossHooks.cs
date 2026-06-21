using HarmonyLib;
using Pipistrello;

namespace PipistrelloAP.Hooks;

[HarmonyPatch(typeof(Scripting.ExternalFunctions), nameof(Scripting.ExternalFunctions.BossEnd))]
public static class BossEndPatch
{
    public static void Postfix()
        => Plugin.Log.LogInfo("[AP] BOSS DEFEATED");
}
