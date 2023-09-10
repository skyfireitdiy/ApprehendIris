from YiYan.YiYanLLM import YiYanLLM
from YiYan.YiYanConfig import YiYanConfig

class YiYanUI(YiYanLLM):
    def __init__(self):
        super(YiYanUI, self).__init__()


    def GetConfig(self):
        ui = YiYanConfig()
        if ui.exec():
            config = ui.GetConfig()
            self.SetConfig(config)
            return config
        return None
