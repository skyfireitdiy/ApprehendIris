import sys
import os
from flask import Flask,  request


file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(file_dir,".."))

from Spark.SparkLLM import Spark


app = Flask(__name__)

@app.route("/spark", methods=['POST'])
def spark():
    # 读取json
    json_body = request.get_json(force=True)
    print(json_body)
    auth = json_body["auth"]
    message = json_body["message"]
    s = Spark(auth["appid"], auth["api_secret"], auth["api_key"])
    return s.Request(message)


