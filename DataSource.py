from Document import Document


class DataSource:
    def CreateDocument(self) -> Document:
        raise NotImplementedError("method not implemented")

    def SetConfig(self, config):
        return None

    def GetConfig(self):
        return None

    def Configed(self):
        return False
