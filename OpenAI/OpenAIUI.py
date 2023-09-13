from OpenAI.OpenAILLM import OpenAILLM
from UI.LineInput import GetLineInput

class OpenAIUI(OpenAILLM):
    def __init__(self):
        super(OpenAIUI, self).__init__()

    def Chat(self, messages) -> str:
        return super().Chat([
                {"role": "user", "content": '\n'.join(messages)}
            ])

    def GetConfig(self) -> str:
        line, ret = GetLineInput("OpenAI API KEY", "OpenAI API KEY", "请输入OpenAI API KEY", True)
        if line and ret:
            config = {
                "api_key": line
            }
            self.SetConfig(config)
            print(config)
            return config
        return None
