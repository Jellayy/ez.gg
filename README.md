![EZ.GG Banner](img/readme-banner.png)
<br><br>
Have you ever been in a League of Legends queue or in the middle of champion select when it suddenly hits you: I wish I could grab a snack right now but what if I miss queue? What if I dont lock in my champion in time? EZ.GG (formerly known as SnackTime) is the ultimate League of Legends queuing to champion select toolkit.
## Demo
![EZ.GG Demo](img/Animation.gif)
## Features
EZ.GG can:
 - Put you into any queue type
 - Select your roles
 - Accept queue pop
 - Ban champions
 - Select your champion
 - Set your runes and summoner spells
 - And more! (maybe)
## Installation & Usage
 EZ.GG is currently in unreleased alpha. Once we are feature complete for version 1, there will be a packaged release.
 <br><br>
 If you want to test/use EZ.GG in the meantime, clone the repo using the commands below:
 ```
git clone https://github.com/Jellayy/ez.gg
cd ez.gg
pip install -r requirements.txt
python driver.py
 ```
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
<sub>If Riot for some reason blocks the API calls their own client frontend uses, we WILL remake this with machine vision out of spite. Come at us riot (with job offers).<sub>
## Contributing
Go ahead.