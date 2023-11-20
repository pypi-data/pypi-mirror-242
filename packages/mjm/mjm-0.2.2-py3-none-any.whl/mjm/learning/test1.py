import sys
# print(sys.modules)
import os
# print(os.getcwd())
import sys,os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#存放c.py所在的绝对路径
# from ..read_tools.按行读取文件转换表格.py import read_data
print(BASE_DIR)
# sys.path.append(BASE_DIR)

# from read_tools.read_table import read_data


# a = read_data("../read_tools/input_data.txt")
# print(a)