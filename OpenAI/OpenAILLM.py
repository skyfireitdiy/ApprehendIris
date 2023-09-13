from Model import Model

import openai


class OpenAILLM(Model):
    def __init__(self):
        super(OpenAILLM, self).__init__()

        self.configed = False
        self.api_key = ""

    def Chat(self, messages) -> str:
        if not self.configed:
            return messages

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return [response["choices"][0]["message"]["content"]]

    def GetConfig(self) -> str:
        return {
            "api_key": self.api_key
        }

    def SetConfig(self, config: dict):
        self.api_key = config["api_key"]
        openai.api_key = self.api_key
        self.configed = True

    def Configed(self):
        return self.configed

    def Description(self):
        return "OpenAI"
