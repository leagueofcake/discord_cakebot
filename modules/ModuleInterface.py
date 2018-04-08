class ModuleInterface:
    def __init__(self):
        self.client = None
        self.conn = None
        self.c = None

        self.logger = None
        self.command_handlers = {}
        self.help_entries = {}

    # Overwritten by PermissionsModule if loaded, otherwise defaults to this
    def auth_function(self, f, *args, **kwargs):
        async def ret_fun(message, *args, **kwargs):
            await f(message)
        return ret_fun

    async def say(self, channel, message):
        pass

    async def temp_message(self, channel, message, time=5):
        pass

    async def delete(self, message):
        pass
