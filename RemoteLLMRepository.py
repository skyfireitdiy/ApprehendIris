import os
import pickle
from RemoteLLM import RemoteLLM


class RemoteLLMRepository:
    def __init__(self, filename):
        self._filename = filename
        self._data = {}
        self._load()

    def _load(self):
        if not os.path.exists(self._filename):
            self._save()

        with open(self._filename, 'rb') as fp:
            self._data = pickle.load(fp)


    def _save(self):
        with open(self._filename, 'wb') as f:
            pickle.dump(self._data, f)

    def GetLLM(self, name):
        if name not in self._data:
            return None
        return self._data[name]

    def AddLLM(self, llm):
        if llm.Name() in self._data:
            raise Exception(f"LLM {llm.Name()} already exists")
        self._data[llm.Name()] = llm
        self._save()

    def DeleteLLM(self, name):
        llm = self.GetLLM(name)
        if llm is None:
            return 
        self._save()

    def UpdateLLM(self, llm, add_if_not_exist=True):
        if add_if_not_exist:
            self._data[llm.Name()] = llm
            return
        if llm.Name() not in self._data:
            raise Exception(f"LLM {llm.Name()} not found")
        self._data[llm.Name()] = llm

    def GetAllLLM(self):
        return self._data.keys()

    def Save(self):
        self._save()

