from pyspark.sql import SparkSession
import time
# https://github.com/aliyun/MaxCompute-Spark/wiki/06.-PySpark-%E8%AE%BF%E9%97%AE-Oss
spark = SparkSession.builder.appName('testoss').getOrCreate()
sc = spark.sparkContext
conf = sc._jsc.hadoopConfiguration()
conf.set("fs.oss.accessKeyId", "LTAI4GLAUYbsDT6uzVpmcSeo")
conf.set("fs.oss.accessKeySecret", "bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU")
conf.set("fs.oss.endpoint", "oss-cn-shenzhen.aliyuncs.com")
conf.set("fs.oss.impl", "org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem")
print("-------------------------------------------start---------------------------------------------")
path = sc._jvm.org.apache.hadoop.fs.Path("oss://bigdata-log-report/log/rp_nginx03/service/20230909/")
fs = sc._jvm.org.apache.hadoop.fs.FileSystem.get(path.toUri(), conf)
exist = fs.exists(path) # 判断目录是否存在
# size = fs.getContentSummary(path).getLength() # 获取文件大小（以字节为单位）
print(exist)
print(time.time())
print("-------------------------------------------stop----------------------------------------------")