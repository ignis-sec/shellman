# shellman
`shellman` (from shell manager) is a modular reverse shell server. The idea is to have a way to manage multiple shells
that a team can use together from modular frontends (like Discord) during a CTF. 

Please check out [the frontends' READMEs][discord_frontend] for information specific to them.

## Demo
Here's what the Discord frontend looks like in action:
<p align="center">
  <img src="shellman/frontends/discord_frontend/demo.gif">
</p>


## Usage
`shellman` only supports Python 3.8+

```
$ python -m shellman
```

It will ask for all the required config, then load all the frontends in `shellman/frontends/`.

## Configuration
Although `shellman` asks you for all the necessary config on launch, you can find and manually edit the config in
 `./config.ini`. Frontend config should also be here.

[![asciicast](https://asciinema.org/a/Yby2HlUeNFLh6YvdSahQe3ggQ.svg)](https://asciinema.org/a/Yby2HlUeNFLh6YvdSahQe3ggQ)


## Disclaimers
- This project is for educational purposes only. The developers and contributors are not responsible for any damage 
that may be caused by this program nor any consequences that may arise.


## Acknowledgements:
- Props to [goeo][goeo_] for his async skills.


[goeo_]: https://github.com/goeo-
[discord_frontend]: https://github.com/FlameOfIgnis/shellman/tree/master/shellman/frontends/discord_frontend