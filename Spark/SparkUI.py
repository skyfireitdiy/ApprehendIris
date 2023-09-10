from Spark.SparkLLM import Spark
from Spark.SparkConfig import SparkConfig


class SpackUI(Spark):
    def __init__(self):
        super(SpackUI, self).__init__()

    def GetConfig(self):
        ui = SparkConfig()
        if ui.exec():
            config = ui.GetConfig()
            self.SetConfig(config)
            return config
        return None
