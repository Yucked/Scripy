using System.Collections.Generic;
using System.Threading.Tasks;
using Discord;
using Discord.WebSocket;
using Microsoft.Extensions.Logging;
using Victoria;
using Victoria.EventArgs;

namespace YOUR_PROJECT.Managers {
    public sealed class MusicManager {
        private readonly LavaNode _lavaNode;
        private readonly ILogger _logger;
        public readonly HashSet<ulong> VoteQueue;

        public MusicManager(DiscordSocketClient socketClient, LavaNode lavaNode, ILogger<MusicManager> logger) {
            socketClient.Ready += OnReady;
            _lavaNode = lavaNode;
            _logger = logger;
            
            _lavaNode.OnLog += OnLog;
            _lavaNode.OnPlayerUpdated += OnPlayerUpdated;
            _lavaNode.OnStatsReceived += OnStatsReceived;
            _lavaNode.OnTrackEnded += OnTrackEnded;
            _lavaNode.OnTrackException += OnTrackException;
            _lavaNode.OnTrackStuck += OnTrackStuck;
            _lavaNode.OnWebSocketClosed += OnWebSocketClosed;

            VoteQueue = new HashSet<ulong>();
        }

        private Task OnLog(LogMessage arg) {
            _logger.Log(arg.Severity.Convert(), arg.Exception, arg.Message);
            return Task.CompletedTask;
        }

        private Task OnPlayerUpdated(PlayerUpdateEventArgs arg) {
            _logger.LogInformation($"Player update received for {arg.Player.VoiceChannel.Name}.");
            return Task.CompletedTask;
        }

        private Task OnStatsReceived(StatsEventArgs arg) {
            _logger.LogInformation($"Lavalink Uptime {arg.Uptime}.");
            return Task.CompletedTask;
        }

        private async Task OnTrackEnded(TrackEndedEventArgs args) {
            if (!args.Reason.ShouldPlayNext())
                return;

            var player = args.Player;
            if (!player.Queue.TryDequeue(out var queueable)) {
                await player.TextChannel.SendMessageAsync("No more tracks to play.");
                return;
            }

            if (!(queueable is LavaTrack track)) {
                await player.TextChannel.SendMessageAsync("Next item in queue is not a track.");
                return;
            }

            await args.Player.PlayAsync(track);
            await args.Player.TextChannel.SendMessageAsync(
                $"{args.Reason}: {args.Track.Title}\nNow playing: {track.Title}");
        }

        private Task OnTrackException(TrackExceptionEventArgs arg) {
            _logger.LogCritical($"Track exception: {arg.ErrorMessage}");
            return Task.CompletedTask;
        }

        private Task OnTrackStuck(TrackStuckEventArgs arg) {
            _logger.LogError($"Track stuck: {arg.Threshold}.");
            return Task.CompletedTask;
        }

        private Task OnWebSocketClosed(WebSocketClosedEventArgs arg) {
            _logger.LogCritical($"Discord WebSocket connection closed with following reason: {arg.Reason}");
            return Task.CompletedTask;
        }

        private async Task OnReady() {
            await _lavaNode.ConnectAsync();
        }
    }
}