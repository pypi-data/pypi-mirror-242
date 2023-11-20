from flask import Flask, request, json
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    # 获取后端人员发送的数据
    data = request.get_data()
    # 将数据转换为字典格式
    data_dict = json.loads(data)
    # 对数据进行处理和验证
    if 'name' in data_dict and 'age' in data_dict:
        # 返回成功的结果
        return json.dumps({'status': 'success', 'message': 'Hello, {}! You are {} years old.'.format(data_dict['name'], data_dict['age'])})
    else:
        # 返回失败的结果
        return json.dumps({'status': 'fail', 'message': 'Invalid data.'})

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)