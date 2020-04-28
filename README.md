# shellman
`shellman` (from shell manager) is a modular reverse shell server. The idea is to have a way to manage multiple shells
that a team can use together from modular frontends (like Discord) during a CTF. 

Please check out the frontends' READMEs for information specific to them.

## Usage
`shellman` only supports Python 3.8+

```
$ python -m shellman
```

It will ask for all the required config, then load all the frontends in `shellman/frontends/`.

## Configuration
Although `shellman` asks you for all the necessary config on launch, you can find and manually edit the config in
 `./config.ini`. Frontend config should also be here.

## Disclaimers
- This project is for educational purposes only. The developers and contributors are not responsible for any damage 
that may be caused by this program nor any consequences that may arise.

## Acknowledgements:
- Props to [goeo][goeo_] for his async skills


[goeo_]: https://github.com/goeo-