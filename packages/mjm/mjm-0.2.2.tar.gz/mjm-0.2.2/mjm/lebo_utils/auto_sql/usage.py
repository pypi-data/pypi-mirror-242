import re
def re_explanatory(param):
    


EXT_OPT="""
set odps.sql.python.version=cp37;
"""
def un_sql(param,ext_opt=None,mod='all'):
    param = "\n" + param
    # 1.支持注释,把所有注释都替换为空
    param=re.sub("(#\s*name.*)(?=\n)",'',param)
    # 2.缺个
    arr=list( filter( lambda x:x.strip()!='', re.split("\n(?=input:)|\n(?=cube:)",param)))
    if ext_opt is not None:
        sqls=ext_opt
    else:
        sqls=EXT_OPT
    # 3.预留模式筛选,这个是设计阶段考虑的，即使你只做了一种模式，也可以先设计，这里有cdc模式和all模式
    for p in arr:
        if mod=='cdc': p=add_cdc(p)
        #print(p)
        sql=sql_rt(p)
        sqls.append(sql)
