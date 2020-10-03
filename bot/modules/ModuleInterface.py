class ModuleInterface:
    def __init__(self):
        self.client = None
        self.conn = None
        self.c = None

        self.modules = set()
        self.logger = None
        self.command_handlers = {}
        self.help_entries = {}

    # Overwritten by PermissionsModule if loaded, otherwise defaults to this
    def auth_function(self, f, *args, **kwargs):
        async def ret_fun(message, *args, **kwargs):
            await f(message)

        return ret_fun
