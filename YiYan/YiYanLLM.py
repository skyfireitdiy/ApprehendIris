from Model import Model


# 填充API Key与Secret Key
import requests
import json


class YiYanLLM(Model):
    def __init__(self):
        super(YiYanLLM, self).__init__()
        self.api_key = ""
        self.secret_key = ""
        self.token = ""
        self.configed = False

    def MakeTokenUrl(self)->str:
        if not self.configed:
            return ""
        return f"https://aip.baidubce.com/oauth/2.0/token?client_id={self.api_key}&client_secret={self.secret_key}&grant_type=client_credentials"

    def Chat(self, messages)->str:
        if not self.configed:
            return messages
        if not self.token:
            self.token = self.GetToken()
            if not self.token:
                return messages
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + self.token
        payload = json.dumps({
            "messages": messages
            })
        headers = {
                'Content-Type': 'application/json'
                }
        response = requests.request("POST", url, headers=headers, data=payload)
        return [json.loads(response.text)["result"]]


    def GetToken(self)->str:
        payload = json.dumps("")
        headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
                }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json().get("access_token")

    def GetConfig(self):
        return {
                "api_key": self.api_key,
                "secret_key": self.secret_key
                }

    def Configed(self):
        return self.configed

    def SetConfig(self, config):
        self.api_key = config["api_key"]
        self.secret_key = config["secret_key"]
        self.configed = True

    def Description(self)->str:
        return "文心一言大模型"


