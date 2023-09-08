from Spark.SparkLLM import Spark
from Spark.SparkConfig import SparkConfig


class SpackUI(Spark):
    def GetConfig(self):
        ui = SparkConfig()
        if ui.exec():
            config = ui.GetConfig()
            self.SetConfig(config)
            return config
        return None
