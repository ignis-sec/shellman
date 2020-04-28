config_dict = {
    'discord_frontend': {
        'token': {
            'default': '',
            'desc': 'Discord token to run the bot.'
        },
        'admin_mode': {
            'default': True,
            'desc': 'Whether the bot will be run as an admin - changes functionality significantly.'
        },
        'guild': {
            'default': 702911703301619742,
            'desc': 'Discord guild (server) to use as a Shellman frontend. Input the snowflake id.'
        },
        'channel': {
            'default': 702911703301619746,
            'desc': 'A "main channel" to run commands that aren\'t related to a specific shell. '
                    'Input the snowflake id.'
        },
        'category': {
            'default': 'shells',
            'desc': 'Category for the bot to create new channels in (only in admin mode).'
                    'Input the name.'
        },
        'channel_scheme': {
            'default': 'shellman-'
                       '{shell.connection.writer.get_extra_info("peername")[0].replace(".", "-")}-'
                       '{shell.connection.id}',
            'desc': 'A channel naming scheme to create new shell channels based on (only in admin mode).'
        },
    }
}