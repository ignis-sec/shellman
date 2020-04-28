import asyncio

from .shellman import ShellmanCore
from .wizard import shellman_wizard, check_config, config_dict
from .config import Config

# check if config has all required keys
if not check_config(config_dict):
    shellman_wizard()

core = ShellmanCore()
core.import_frontends()

loop = asyncio.get_event_loop()

loop.create_task(core.start_listening(Config()['shellman']['host'], Config()['shellman']['port']))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(ShellmanCore().shutdown())
finally:
    print('Shutting down')
    loop.close()
