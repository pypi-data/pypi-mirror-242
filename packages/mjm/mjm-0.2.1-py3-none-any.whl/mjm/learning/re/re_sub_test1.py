import re
import logging
s = "您好，欢迎来到我的博客：https://blog.csdn.net/weixin_44799217,,,###,,,我的邮箱是：535646343@qq.com. Today is 2021/12/21. It is a wonderful DAY!"
 

#re.sub练习
# 从源码中看出re.sub()函数共有5个参数：
# pattern：表示正则中的模式字符串；
# repl：表示要替换的字符串（即匹配到pattern后替换为repl），也可以是个函数；
# string：表示要被处理（查找替换）的原始字符串；
# count：可选参数，表示要替换的最大次数，而且必须是非负整数，该参数默认为0，即所有的匹配都会替换；
# flags：可选参数，表示编译时用的匹配模式（如忽略大小写、多行模式等），数字形式，默认为0。
# ————————————————
# 版权声明：本文为CSDN博主「IT之一小佬」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/weixin_44799217/article/details/115100715

#  只匹配单一数字
print("只匹配单一数字(:")
ret = re.sub(r'[0-9]', "*", s)
print(ret)

#  只匹配单一字母(小写)
print("只匹配单一字母(小写):")
ret2 = re.sub(r'[a-z]',"*", s)
print(ret2)

# 匹配单一数字和字母
print("匹配单一数字和字母(:")
ret3 = re.sub(r'[0-9a-z]',"*", s)
print(ret3)
ret4 = re.sub(r'[0-9a-zA-Z]', "*", s)
print(ret4)

# 匹配多个字母
print("匹配多个字母(:")
ret5 = re.sub(r'[a-zA-Z]+',"*",s)
print(ret5)

# 匹配多个连续数字和字母
print("匹配多个连续数字和字母(:")
ret6 = re.sub(r'[0-9a-zA-Z]+',"*",s)
print(ret6)


# 匹配非数字
print("匹配非数字(:")
ret7 = re.sub(r'[^0-9]', "*", s)
print(ret7)


# 把以#   name开头的，以\n结尾的注释删除掉
print("dsl自定义注释(:")
ret8 = """
# name123
true
# name345
false
"""
print("注释前:",ret8)
ret8=re.sub("(#\s*name.*)(?=\n)",'',ret8)
print("注释后:",ret8)






