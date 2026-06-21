using System.Threading;
using Archipelago.MultiClient.Net;
using Archipelago.MultiClient.Net.Enums;
using Archipelago.MultiClient.Net.Helpers;
using Archipelago.MultiClient.Net.Packets;

namespace PipistrelloAP.Archipelago;

public static class ArchipelagoClient
{
    public const string APVersion = "0.5.1";
    const string GameName = "Pipistrello and the Cursed Yoyo";

    static ArchipelagoSession? _session;
    static bool _attemptingConnection;

    public static bool Authenticated { get; private set; }
    public static ArchipelagoData ServerData { get; } = new();

    // ── Connection ──────────────────────────────────────────────────────────

    public static void Connect()
    {
        if (Authenticated || _attemptingConnection) return;
        _attemptingConnection = true;

        try
        {
            _session = ArchipelagoSessionFactory.CreateSession(ServerData.Uri);
            RegisterHandlers();
            ThreadPool.QueueUserWorkItem(_ => TryLogin());
        }
        catch (Exception e)
        {
            Plugin.Log.LogError($"[AP] Failed to create session: {e.Message}");
            _attemptingConnection = false;
        }
    }

    public static void Disconnect()
    {
        _session?.Socket.DisconnectAsync();
        _session = null;
        Authenticated = false;
        Plugin.Log.LogInfo("[AP] Disconnected.");
    }

    // ── Outgoing ────────────────────────────────────────────────────────────

    public static void SendLocationCheck(long locationId)
    {
        if (!Authenticated || _session == null)
        {
            Plugin.Log.LogWarning($"[AP] Not connected — queued check {locationId} for resync on reconnect");
            return;
        }
        _session.Locations.CompleteLocationChecksAsync(locationId);
    }

    public static void Say(string message) =>
        _session?.Socket.SendPacketAsync(new SayPacket { Text = message });

    // ── Private helpers ─────────────────────────────────────────────────────

    static void RegisterHandlers()
    {
        _session!.MessageLog.OnMessageReceived += msg =>
            Plugin.Log.LogInfo($"[AP] {msg}");

        _session.Items.ItemReceived += OnItemReceived;
        _session.Socket.ErrorReceived += OnSocketError;
        _session.Socket.SocketClosed += OnSocketClosed;
    }

    static void TryLogin()
    {
        try
        {
            var result = _session!.TryConnectAndLogin(
                GameName,
                ServerData.SlotName,
                ItemsHandlingFlags.AllItems,
                new Version(APVersion),
                password: ServerData.Password,
                requestSlotData: true
            );
            HandleConnectResult(result);
        }
        catch (Exception e)
        {
            Plugin.Log.LogError($"[AP] Login error: {e.Message}");
            HandleConnectResult(new LoginFailure(e.Message));
        }
        finally
        {
            _attemptingConnection = false;
        }
    }

    static void HandleConnectResult(LoginResult result)
    {
        if (result.Successful)
        {
            var success = (LoginSuccessful)result;
            ServerData.SetupSession(success.SlotData, _session!.RoomState.Seed);
            Authenticated = true;

            Plugin.Log.LogInfo($"[AP] Connected to {ServerData.Uri} as '{ServerData.SlotName}' — seed {_session.RoomState.Seed}");

            // Resync any locations checked while offline
            if (ServerData.CheckedLocations.Count > 0)
            {
                Plugin.Log.LogInfo($"[AP] Resyncing {ServerData.CheckedLocations.Count} offline check(s)...");
                _session.Locations.CompleteLocationChecksAsync(ServerData.CheckedLocations.ToArray());
            }
        }
        else
        {
            var failure = (LoginFailure)result;
            var errors = string.Join(", ", failure.Errors);
            Plugin.Log.LogError($"[AP] Connection refused: {errors}");
            Authenticated = false;
        }
    }

    // ── Incoming ────────────────────────────────────────────────────────────

    static void OnItemReceived(ReceivedItemsHelper helper)
    {
        while (helper.Any())
        {
            var item = helper.DequeueItem();

            // Skip items we already processed in a previous session
            if (helper.Index <= ServerData.Index) continue;
            ServerData.Index++;

            Plugin.Log.LogInfo($"[AP] Item received: {item.ItemName} (id {item.ItemId})");
            // TODO Phase 3: ItemManager.GrantItem(item.Item);
        }
    }

    static void OnSocketError(Exception e, string message)
    {
        Plugin.Log.LogError($"[AP] Socket error — {message}: {e.Message}");
    }

    static void OnSocketClosed(string reason)
    {
        Plugin.Log.LogWarning($"[AP] Connection closed: {reason}");
        Authenticated = false;
    }
}
