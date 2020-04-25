import asyncio

from .shellman import ShellmanCore
from .wizard import shellman_wizard
from .config import Config

# check if config exists
try:
    Config()['shellman']
except KeyError:
    shellman_wizard()

core = ShellmanCore()
core.import_frontends()

loop = asyncio.get_event_loop()

loop.create_task(core.start_listening(Config()['connection']['host'], Config()['connection']['port']))
try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(ShellmanCore().shutdown())
finally:
    print('Shutting down')
    loop.close()
