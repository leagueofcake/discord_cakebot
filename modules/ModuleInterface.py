class ModuleInterface:
    def __init__(self):
        self.client = None
        self.conn = None
        self.c = None

        self.logger = None
        self.command_handlers = {}

    def auth_function(self, f):
        pass

    async def say(self, channel, message):
        pass

    async def temp_message(self, channel, message, time=5):
        pass

    async def delete(self, message):
        pass
