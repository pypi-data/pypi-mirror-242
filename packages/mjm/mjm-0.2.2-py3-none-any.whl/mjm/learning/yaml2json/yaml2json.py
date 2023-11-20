import yaml
import json
# 
param1 = """
input1:
    abc
"""

param2 = """
input1:
    name: zhangsan
    age: 123
"""

param3 = """
fruits:
    - "苹果"
    - "西瓜"
    - "葡萄"
"""

param3 = """
fruits:
    - "苹果"
    - "西瓜"
    - "葡萄"
"""

param4 = """
fruits:
    - 苹果
      - 富士康苹果
      - 大苹果
    - 西瓜
    - 葡萄
"""


for i in range(1,5):
    print("----------------------demo%d----------------------" % i)
    str1 = "param" + str(i)
    print(eval(str1))
    cfg = yaml.load(eval(str1),yaml.FullLoader)
    print("result:\n%s" % cfg)
    
