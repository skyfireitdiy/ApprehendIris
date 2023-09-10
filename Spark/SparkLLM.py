from Spark import SparkApi
from Model import Model

# 用于配置大模型版本，默认“general/generalv2”
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


class Spark(Model):
    def __init__(self):
        super().__init__()
        self._appid = ""
        self._api_secret = ""
        self._api_key = ""
        self._configed = False
        self._domain = "general"   # v1.5版本
        # self._domain = "generalv2"    # v2.0版本

    def Chat(self, message) -> str:
        return [SparkApi.Request(self._appid, self._api_key, self._api_secret, Spark_url, self._domain, [{
            "role": "user",
            "content": '\n'.join(message)
            }])]

    def GetConfig(self):
        return {
                "api_secret": self._api_secret,
                "api_key": self._api_key,
                "appid": self._appid
                }

    def SetConfig(self, config):
        self._appid = config["appid"]
        self._api_secret = config["api_secret"]
        self._api_key = config["api_key"]
        self._configed = True

    def Configed(self):
        return self._configed

    def Description(self):
        return "讯飞星火大模型"
