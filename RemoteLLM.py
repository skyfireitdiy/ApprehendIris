from Entity import Entity
from LLM import LLM
import json
import requests

class RemoteLLM(LLM):
    def __init__(self, name, url, auth_key):
        super().__init__()
        self.name = name
        self.url = url
        self.auth_key = auth_key
        self.authed = False
        self.auth_info= {}

    def Jsonfiy(self):
        return json.dumps({'name': self.name, 'url': self.url, 'authed':self.authed ,
                           'auth_key': self.auth_key, 'id':self.ID(), 
                           'auth_info': self.auth_info})

    def SetAuthed(self, authed):
        self.authed = authed

    def SetAuthInfo(self, auth_info):
        for k in self.auth_key:
            if k not in auth_info:
                raise Exception(f"key {k} not found in auth_info")
        self.auth_info = auth_info
        self.authed = True

    def AuthInfo(self):
        return self.auth_info

    def Name(self):
        return self.name

    def Url(self):
        return self.url

    def AuthKey(self):
        return self.auth_key

    def Request(self, message):
        data = {
                "auth": self.auth_info,
                "message": message
                }
        try:
            return requests.post(self.url, json=data).content.decode()
        except Exception as e:
            return f"LLM interface error: {e}"
