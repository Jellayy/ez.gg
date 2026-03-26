![EZ.GG Banner](img/readme-banner.png)
<br><br>
Have you ever been in a League of Legends queue or in the middle of champion select when it suddenly hits you: I wish I could grab a snack right now but what if I miss queue? What if I dont lock in my champion in time? EZ.GG is the ultimate League of Legends companion app to make the queuing and champion select experience better — now as a fast, dependency-free terminal UI written in Go.

## Features
EZ.GG can:
 - Automatically accept queue pop
 - Smartly ban champions (skips teammate hovers)
 - Lock in your champion
 - Set your runes and summoner spells (via op.gg recommendations)
 - And more! (maybe)

## Installation & Usage

### Prebuilt binaries
Head over to the [releases tab](https://github.com/Jellayy/ez.gg/releases) for pre-built binaries.

### Build from source
Go 1.21+ is required.

```sh
git clone https://github.com/Jellayy/ez.gg
cd ez.gg
go build -o ezgg .
./ezgg
```

### Controls
| Key | Action |
|-----|--------|
| `Tab` / `Shift-Tab` | Navigate between settings |
| `Space` / `Enter` | Toggle a boolean setting |
| Type | Edit the focused text field (champion name / bans) |
| `Esc` | Leave a text field |
| `q` / `Ctrl-C` | Quit |

### Configuration
Settings are saved automatically to `~/.config/ezgg/config.json` when you change them in the TUI.

## Riot TOS
Not gonna lie I haven't read the TOS for external tools on league, but I'm pretty sure the autopilot feature is against TOS.
<br><br>
Do we care?
<br>
No.
<br><br>
But in all reality, as undocumented as they are, the client API endpoints used in EZ.GG are exactly as accessible as the ones Riot does allow other tools to use. The great part about EZ.GG is we aren't distributing this closed-source for monetization. This is open-source software you're either downloading or pulling yourself. I'd love to see Riot try and throw a takedown at open-source software using openly available API calls.
<br><br>
However, for the sake of your own Riot account, use at your own risk.
<br><br>
If anyone at Riot happens to be reading this, if you could accidentally send over a dev Client/LCU API that'd be great. Then we wouldn't have to actively degrade your game quality by dodging 30 games in a row just to test one feature.
<br><br>
<sub>If Riot for some reason blocks the API calls their own client frontend uses, we WILL remake this with machine vision out of spite. Come at us riot (with job offers).<sub>

## Bug Reporting
If you run into an issue while using EZ.GG, we encourage you to open issues to help us improve the app!
<br><br>
In order to ensure enough information is provided to diagnose or reproduce the issue, please include any applicable screenshots and logs from your session. EZ.GG's logs can be found in the user/home folder of your respective platform:
```
~/ezgg-logs.txt
```

## Contributing
Go ahead.