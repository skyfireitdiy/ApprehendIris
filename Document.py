import uuid
from Entity import Entity


class DocumentType:
    Text = 0
    Url = 1
    Doc = 2
    Pdf = 3
    PlainText = 4
    Browser = 5


class Document(Entity):
    def __init__(self, type_: DocumentType):
        super().__init__()
        self._type = type_
        self._cache = ""

    def GetText(self) -> str:
        if not self.Cached():
            return self.Read()
        if not self._cache:
            self._cache = self.Read()
        return self._cache

    def ForceGetText(self) -> str:
        self._cache = ""
        return self.GetText()

    def Name(self) -> str:
        return ""

    def Read(self) -> str:
        raise NotImplementedError("this method is not implemented")

    def Cached(self) -> bool:
        return True
