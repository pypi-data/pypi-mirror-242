import re

# 将按照中文123input:的方式进行切割
ret1 = "中文123input:123"
ret1 = re.split("[0-9]*input:",ret1)
print(ret1)