# discord_frontend
`discord_frontend` is a frontend module for `shellman`. The idea is that it lets you (and your team) control your `shellman` reverse shells over Discord. Also, we like using Discord as 
[@excusemewtf_ctf][excusemewtf].

## Usage
```
$ pip install -r requirements.txt
```
You can then run `shellman`. It will ask for all the required config. You can run `!help` in the chosen "main channel"
to get information regarding the commands.


## Configuration
To use `discord_frontend`, create a new server or be a part of a Discord server where you are an admin. Afterwards go to 
[Discord Developer Portal][Discord Developer Portal] and create a new application. In your application's settings, go 
to the `Bot` tab and turn your application into a bot. Then optionally (if you want to enable admin mode), go to the 
`OAuth` tab and tick `Bot` in `Scopes` and `Administrator` in `Bot Permissions`. Then, use the generated link to add the
bot to your server.

Finally, copy `Token` in `Bot` tab of [Discord Developer Portal][Discord Developer Portal] and paste the said info when 
asked.

## An explanation of "admin mode"
In admin mode, `discord_frontend` will automatically listen to each new `shellman` connection, and create a channel for 
it in the configured category with a name created by running the `channel_scheme` configured as a Python f-string. 

The commands `!clear`, `!rename`, `!catreset` are only enabled in admin mode.

The bot likely doesn't actually need the "Administrator" permission - the "Manage Channels" permission should be enough,
although we've only tested with "Administrator", and the security impact of compromise wouldn't be very different.

## Disclaimers
- This project is for educational purposes only. The developers and contributors are not responsible for any damage 
that may be caused by this program nor any consequences that may arise.
- By using this program you accept that the developers and contributors are not responsible if you violate 
[Discord's Terms of Service][Discord ToS], [Discord's API Terms of Service][Discord API ToS].

## Acknowledgements:
- Props to [goeo][goeo_] for his async skills


[excusemewtf]: https://twitter.com/excusemewtf
[Discord Developer Portal]: https://discordapp.com/developers/applications
[Discord ToS]:              https://discordapp.com/terms
[Discord API ToS]:          https://discordapp.com/developers/docs/legal
[goeo_]: https://github.com/goeo-
