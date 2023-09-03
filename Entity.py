import uuid

class Entity:
    def __init__(self, id=None):
        if id is None:
            self._id = uuid.uuid4().hex 
        else:
            self._id = id


    def SetID(self, id):
        self._id=id

    def ID(self):
        return self._id
