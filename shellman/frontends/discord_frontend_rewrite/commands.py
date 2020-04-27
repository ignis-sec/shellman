import re

from .handlers import send_to_shell, send_ctrl_c, flush, clear, reset_category, listen_shell,\
                      listen_server, list_shells, list_servers, close_server, close_shell, rename_channel,\
                      main_channel_help, shell_channel_help


# Set what handles which regexes
main_channel_commands = {
    r'^!catreset$': reset_category,
    r'^!listen( (\d+) <#(\d+)>)?$': listen_shell,
    r'^!shells$': list_shells,
    r'^!serverlisten( (\S+) (\d{1,5}))?$': listen_server,
    r'^!serverclose( (\S+) (\d{1,5}))?$': close_server,
    r'^!servers$': list_servers,
    r'^!help$': main_channel_help
}

shell_commands = {
    r'^(!|\^)C$': send_ctrl_c,
    r'^!flush$': flush,
    r'^!clear$': clear,
    r'^!close$': close_shell,
    r'^!rename( (\S+))?$': rename_channel,
    r'^!help$': shell_channel_help,
    r'^.*$': send_to_shell
}

# Compile the regexes so they run faster (we'll be running them for every command!)
for regex in main_channel_commands.copy():
    main_channel_commands[re.compile(regex)] = main_channel_commands.pop(regex)

for regex in shell_commands.copy():
    shell_commands[re.compile(regex)] = shell_commands.pop(regex)


async def handle_main_channel_command(message, discord_client):
    """
    Tries to match message to regexes in keys of the dict `main_channel_commands`.
    For the first key that matches, the coroutine in the value will be passed message and awaited.
    If nothing matches, nothing will happen.

    :param message: The discord.py Message object to check
    :param discord_client: The discord.py Client
    """
    for regex_, handler in main_channel_commands.items():
        match = regex_.match(message.content)
        if match:
            await handler.handle(message, match, discord_client)
            break


async def handle_shell_command(message, shell, shellman_frontend):
    """
    Tries to match message to regexes in keys of the dict `shell_commands`.
    For the first key that matches, the coroutine in the value will be passed message and awaited.
    If nothing matches, nothing will happen.

    :param message: The discord.py Message object to check
    :param shell: The Shell object the message is for
    :param shellman_frontend: The instance of ShellmanFrontend we come from - this is for letting ShellmanCore
                              notify the other frontends about what we're doing.
    """
    for regex_, handler in shell_commands.items():
        match = regex_.match(message.content)
        if match:
            await handler.handle(message, match, shell, shellman_frontend)
            break
