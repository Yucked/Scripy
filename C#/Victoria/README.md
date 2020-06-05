<p align="center">
	<img src="https://i.imgur.com/OibdkEz.png" />
	</br>
	<a href="https://discord.gg/ZJaVXK8">
		<img src="https://img.shields.io/badge/Discord-Support-%237289DA.svg?logo=discord&style=for-the-badge&logoWidth=20&labelColor=0d0d0d" />
	</a>
	<a href="https://github.com/Yucked/Victoria/actions">
		<img src="https://img.shields.io/github/workflow/status/Yucked/Victoria/Yeehaw%20Workflow?label=BUILD%20STATUS&logo=github&style=for-the-badge&logoWidth=20&color=181717" />
	</a>
	<a href="https://www.nuget.org/packages/Victoria/">
		<img src="https://img.shields.io/nuget/dt/Victoria.svg?label=Downloads&logo=nuget&style=for-the-badge&logoWidth=20&labelColor=0d0d0d" />
	</a>
  	<a href="http://buymeacoff.ee/Yucked">
		<img src="https://img.shields.io/badge/Buy%20Me%20A-Coffee-%23FF813F.svg?logo=buy-me-a-coffee&style=for-the-badge&logoWidth=20&labelColor=0d0d0d" />
	</a>  
	<p align="center">
	     🌋 - Lavalink wrapper for Discord.NET which provides more options and performs better than all .NET Lavalink libraries combined.
  </p>
</p>

---

## `⚗️ Quick Start:`
Depending on which version you want to use, please download the latest package for said version. This will cover v4 and v5.
Please keep few things in mind when working with Victoria.
- There should *ONLY BE ONE* instance of `LavaNode`/`LavaShardedClient`/`LavaSocketClient`/`LavaRestClient` throughout your whole program.
- If you have multiple instances of Lavalink running, you can easily create a pool of `LavaNode`/`LavaShardedClient`/`LavaSocketClient`/`LavaRestClient`.
- If for some reason you aren't using DI (Dependency Injection), you can create a global static instance of said objects above.

### `v4:`
- Depending on which Discord client you are using (DiscordSocketClient/DiscordShardedClient) add either `LavaSocketClient` or `LavaShardedClient` to service `ServiceCollection` (DI).
```cs

	var services = new ServiceCollection()
		// Other services DiscordSocketClient, CommandService, etc
		.AddSingleton<LavaSocketClient>() // For connecting with the Lavalink's websocket.
		.AddSingleton<LavaRestClient>();  // For using Lavalink's REST endpoints such as searching tracks.
		
	var provider = services.BuildServiceProvider();
```

```cs
	discordSocketClient.Ready += OnReadyAsync;
	....
	
	private async Task OnReadyAsync() {
		await _instanceOfLavaSocketClient.StartAsync(discordSocketClient);
		// Other ready related stuff
	}
```


### `v5:`
- Add `LavaNode` and `LavaConfig` to `ServiceCollection`.
```cs
	// For version 5.1.2 and before.

	var services = new ServiceCollection()
		// Other services DiscordSocketClient, CommandService, etc
		.AddSingleton<LavaNode>()
		.AddSingleton<LavaConfig>();
		
	var provider = services.BuildServiceProvider();
```

```cs
	// For versions 5.1.3 and above.
	var services = new ServiceCollection()
		// Other services DiscordSocketClient, CommandService, etc
		.AddLavaNode(x => {
			x.SelfDeaf = true;
		});
		
	var provider = services.BuildServiceProvider();
```

- In your `DiscordSocketClient` or `DiscordShardedClient` `Ready` event call `_instanceOfLavaNode.ConnectAsync();`
- The `_instanceOfLavaNode` should be injected fetched from your Dependency Injection.

```cs
	discordSocketClient.Ready += OnReadyAsync;
	....
	
	private async Task OnReadyAsync() {
	// Avoid calling ConnectAsync again if it's already connected 
	// (It throws InvalidOperationException if it's already connected).
		if (!_instanceOfLavaNode.IsConnected) {
			await _instanceOfLavaNode.ConnectAsync();
		}
		
		// Other ready related stuff
	}
```