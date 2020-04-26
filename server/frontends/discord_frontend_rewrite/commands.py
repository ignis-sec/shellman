import re

from .handlers import send_to_shell

# Set what handles which regexes
main_channel_commands = {}  # TODO: implement main channel commands (listen shell, listen port?, list shells)

shell_commands = {
    r'^.*$': send_to_shell.handler  # TODO: implement shell specific commands (^C, flush, clear)
}

# Compile the regexes so they run faster (we'll be running them for every command!)
for regex in main_channel_commands.copy():
    main_channel_commands[re.compile(regex)] = main_channel_commands.pop(regex)

for regex in shell_commands.copy():
    shell_commands[re.compile(regex)] = shell_commands.pop(regex)


async def handle_main_channel_command(message):
    """
    Tries to match message to regexes in keys of the Dict[re.Pattern, asyncio.Awaitable] `main_channel_commands`.
    If a key matches, the value will be awaited.
    If nothing matches, nothing will happen.

    :param message: The discord.py Message object to check
    """
    for regex_, handler in main_channel_commands.items():
        if regex_.match(message.content):
            await handler(message)


async def handle_shell_command(message, shell, shellman_frontend):
    """
    Tries to match message to regexes in keys of the Dict[re.Pattern, asyncio.Awaitable] `shell_commands`.
    If a key matches, the value will be awaited.
    If nothing matches, nothing will happen.

    :param message: The discord.py Message object to check
    :param shell: The Shell object the message is for
    :param shellman_frontend: The instance of ShellmanFrontend we come from - this is for letting ShellmanCore
                              notify the other frontends about what we're doing.
    """
    for regex_, handler in shell_commands.items():
        if regex_.match(message.content):
            await handler(message, shell, shellman_frontend)
