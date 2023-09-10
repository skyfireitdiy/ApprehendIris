from Entity import Entity


class Model(Entity):
    def __init__(self):
        super().__init__()
        self._progress_callback = None
        self._logger = None

    def Chat(self, messages) -> str:
        raise NotImplementedError("method is not implemented")

    def GetConfig(self):
        return None

    def SetConfig(self, config):
        return None

    def Configed(self):
        return False

    def Description(self):
        return ""

    def SetProgressCallback(self, cb):
        self._progress_callback = cb

    def SetLogger(self, logger):
        self._logger = logger

    def Progress(self, n):
        if self._progress_callback:
            self._progress_callback(n)

    def Log(self, message):
        if self._logger:
            self._logger(message)
