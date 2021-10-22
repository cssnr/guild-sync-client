# Guild Sync Client

Client Application for Guild Sync.

[https://guildsync.cc/](https://guildsync.cc/)

### Download

- Latest for Windows: [GuildSync.exe](https://github.com/cssnr/guild-sync-client/releases/latest/download/GuildSync.exe)
- Latest for macOS: `Coming Soon`  

Or head over to the [Releases page](https://github.com/cssnr/guild-sync-client/releases).

### Running

1. Download and run: `GuildSync.exe`
1. Copy your `Client Access Key` from your Profile on the website (top right corner).
1. Select your WoW WTF Account Folder (just the account name).
   * Example: `C:\Program Files (x86)\World of Warcraft\_classic_\WTF\Account\Test123`
1. Make sure you have run, or do run the in-game addon.
   * [Guild Sync Addon](https://github.com/cssnr/guild-sync-addon)

### Building

```
pyinstaller.exe --clean --console --onefile .\guild-sync.spec
```
