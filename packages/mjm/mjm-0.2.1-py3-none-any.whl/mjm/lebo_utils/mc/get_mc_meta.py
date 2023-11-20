
from odps import ODPS 
import pandas as pd
import os

# https://blog.csdn.net/xiaohutong1991/article/details/107649092
# 显示所有列
pd.set_option('display.max_columns',None)
# 显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.expand_frame_repr',False)

# 阿里云文档链接: 
# https://help.aliyun.com/zh/maxcompute/user-guide/examples-of-using-the-sdk-for-python-tables?spm=a2c4g.11186623.0.0.53162390tsVdUq
# 获取表的所有列名
def query_table_schema(table_name):
    o = ODPS('LTAI4GLAUYbsDT6uzVpmcSeo', 'bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU', 'lebo_data', 'http://service.odps.aliyun.com/api')
    t = o.get_table(table_name)
    return t.schema


# 获取表的某一列的所有枚举值
def query_table_columns_enum(table_name,columns_name,p_date = None,limit = True):
    # https://blog.csdn.net/xiaohutong1991/article/details/107649092
    # 显示所有列
    pd.set_option('display.max_columns',None)
    # 显示所有行
    pd.set_option('display.max_rows',None)
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.expand_frame_repr',False)
    #https://help.aliyun.com/document_detail/90441.html语法参考
    #sql="select * from ods_vip_user_login_detail where p_date='20230208' limit 10 "
    # o = ODPS('LTAI5tDS41sByhnjCCMnz7ze', '6VcacaylxZyDVBowRH7Hj8N94pn4I4', 'lebo_data', 'http://service.odps.aliyun.com/api')
    o = ODPS('LTAI4GLAUYbsDT6uzVpmcSeo', 'bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU', 'lebo_data', 'http://service.odps.aliyun.com/api')
    import datetime,time
    today = datetime.datetime.now()
    delta = datetime.timedelta(days = 1)
    dt = today - delta
    dt = dt.strftime('%Y%m%d')
    dt = f"where   p_date = '{dt}'" if p_date is not None else ''
    limit_sql = 'limit 999' if (limit == True) else ''
    sql = f"""
        select {columns_name} , count(*)
        from    lebo_data.{table_name}
        {dt}
        group by {columns_name}
        {limit_sql}
    """

    with o.execute_sql(sql, hints={'odps.stage.mapper.split.size': 16,"odps.sql.submit.mode" : "script"}).open_reader(tunnel=True) as f:
        df=f.to_pandas()
    return df



# 获取表的某一列的所有枚举值
def query_table_columns_enum2(table_name,columns_name,p_date = None,limit = True):
    # https://blog.csdn.net/xiaohutong1991/article/details/107649092
    # 显示所有列
    pd.set_option('display.max_columns',None)
    # 显示所有行
    pd.set_option('display.max_rows',None)
    pd.set_option('display.max_colwidth', 200)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.expand_frame_repr',False)
    #https://help.aliyun.com/document_detail/90441.html语法参考
    #sql="select * from ods_vip_user_login_detail where p_date='20230208' limit 10 "
    # o = ODPS('LTAI5tDS41sByhnjCCMnz7ze', '6VcacaylxZyDVBowRH7Hj8N94pn4I4', 'lebo_data', 'http://service.odps.aliyun.com/api')
    o = ODPS('LTAI4GLAUYbsDT6uzVpmcSeo', 'bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU', 'lebo_data', 'http://service.odps.aliyun.com/api')
    import datetime,time
    today = datetime.datetime.now()
    delta = datetime.timedelta(days = 1)
    dt = today - delta
    dt = dt.strftime('%Y%m%d')
    dt = f"where   p_date = '{dt}'" if p_date is not None else ''
    limit_sql = 'limit 999' if (limit == True) else ''
    sql = f"""
        select {columns_name} , count(*)
        from    lebo_data.{table_name}
        {dt}
        group by {columns_name}
        {limit_sql}
    """

    with o.execute_sql(sql, hints={'odps.stage.mapper.split.size': 16,"odps.sql.submit.mode" : "script"}).open_reader(tunnel=True) as f:
        df=f.to_pandas()
    return df




# 判断是否存在元数据


# t.lifecycle
# t.is_virtual_view
# t.size
# t.schema.columns
