from Spark import SparkApi
from LLM import LLM

#用于配置大模型版本，默认“general/generalv2”
#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


class Spark(LLM):
    def __init__(self, appid, api_secret, api_key):
        super().__init__()
        self._appid = appid
        self._api_secret = api_secret
        self._api_key = api_key
        self._domain = "general"   # v1.5版本
        # self._domain = "generalv2"    # v2.0版本


    def Chat(self, message)->str:
        return SparkApi.Request(self._appid,self._api_key,self._api_secret,Spark_url,self._domain, [{
            "role": "user",
            "content": message
            }])
    

