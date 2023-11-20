
from odps import ODPS 
import pandas as pd


# https://blog.csdn.net/xiaohutong1991/article/details/107649092
# 显示所有列
pd.set_option('display.max_columns',None)
# 显示所有行
pd.set_option('display.max_rows',None)
pd.set_option('display.max_colwidth', 200)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.expand_frame_repr',False)
def mc_query(sql):
      #https://help.aliyun.com/document_detail/90441.html语法参考
      #sql="select * from ods_vip_user_login_detail where p_date='20230208' limit 10 "
      # o = ODPS('LTAI5tDS41sByhnjCCMnz7ze', '6VcacaylxZyDVBowRH7Hj8N94pn4I4', 'lebo_data', 'http://service.odps.aliyun.com/api')
      o = ODPS('LTAI4GLAUYbsDT6uzVpmcSeo', 'bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU', 'lebo_data', 'http://service.odps.aliyun.com/api')
      with o.execute_sql(sql, hints={'odps.stage.mapper.split.size': 16,"odps.sql.submit.mode" : "script"}).open_reader(tunnel=True) as f:
          df=f.to_pandas()
      return df

sql = """
select  count(distinct uid)
from    lebo_data.dm_haoli_install
where   appid = '22451'
limit 100;
"""

if __name__ == '__main__':
    df = mc_query(sql)
    print(df)

