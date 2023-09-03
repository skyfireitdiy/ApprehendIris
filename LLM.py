from Entity import Entity

class LLM(Entity):
    def __init__(self):
        super().__init__()

    def Request(self, message):
        return self.Chat(message)

    def Chat(self, message)->str:
        raise NotImplementedError("method is not implemented")
