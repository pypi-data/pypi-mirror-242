from pyspark.sql import SparkSession
# spark.serializer要在创建builder的时候就配置否则报错




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
select *
from    lebo_data.dwd_sdk_install_fact
where   dt = '20230628'
limit 100;
"""

if __name__ == '__main__':
    df = mc_query(sql)
    print(df)
    spark = SparkSession.builder.appName('testoss').config("spark.serializer", "org.apache.spark.serializer.KryoSerializer").config('spark.sql.extensions','org.apache.spark.sql.hudi.HoodieSparkSessionExtension').config('spark.sql.hive.convertMetastoreParquet','false').getOrCreate()
    sc = spark.sparkContext
    conf = sc._jsc.hadoopConfiguration()
    conf.set("fs.oss.accessKeyId", "LTAI4GLAUYbsDT6uzVpmcSeo")
    conf.set("fs.oss.accessKeySecret", "bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU")
    conf.set("fs.oss.endpoint", "oss-cn-shenzhen.aliyuncs.com")
    conf.set("fs.oss.impl", "org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem")
    conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    conf.set("spark.sql.extensions","org.apache.spark.sql.hudi.HoodieSparkSessionExtension")
    print("-------------------------------------------start---------------------------------------------")
    # pyspark
    tableName = "hudi_trips_cow_20220925"
    basePath = "oss://big-oss/tmp_mjm/huditest_20220925"
    dataGen = sc._jvm.org.apache.hudi.QuickstartUtils.DataGenerator()
    inserts = sc._jvm.org.apache.hudi.QuickstartUtils.convertToStringList(dataGen.generateInserts(10))
    
    hudi_options = {
        'hoodie.table.name': tableName,
        'hoodie.datasource.write.recordkey.field': 'uuid',
        'hoodie.datasource.write.partitionpath.field': 'partitionpath',
        'hoodie.datasource.write.table.name': tableName,
        'hoodie.datasource.write.operation': 'upsert',
        'hoodie.datasource.write.precombine.field': 'ts',
        'hoodie.upsert.shuffle.parallelism': 2,
        'hoodie.insert.shuffle.parallelism': 2
    }

    df.write.format("hudi"). \
        options(**hudi_options). \
        mode("overwrite"). \
        save(basePath)
    print("-------------------------------------------stop----------------------------------------------")



