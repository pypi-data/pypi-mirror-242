from pyspark.sql import SparkSession
# spark.serializer要在创建builder的时候就配置否则报错
spark = SparkSession.builder.appName('testoss').config("spark.serializer", "org.apache.spark.serializer.KryoSerializer").config('spark.sql.extensions','org.apache.spark.sql.hudi.HoodieSparkSessionExtension').config('spark.sql.hive.convertMetastoreParquet','false').getOrCreate()
sc = spark.sparkContext
conf = sc._jsc.hadoopConfiguration()
conf.set("fs.oss.accessKeyId", "LTAI4GLAUYbsDT6uzVpmcSeo")
conf.set("fs.oss.accessKeySecret", "bRBzwK0VpTM4XyzsP5nSSoqoh8HCIU")
conf.set("fs.oss.endpoint", "oss-cn-shenzhen.aliyuncs.com")
conf.set("fs.oss.impl", "org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem")
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
conf.set("spark.sql.extensions","org.apache.spark.sql.hudi.HoodieSparkSessionExtension")
#
basePath = "oss://big-oss/tmp_mjm/huditest"

#pyspark 创建视图
#时间旅行as.of.instant
spark.read. \
  format("hudi"). \
  option("as.of.instant", "20230925010101000"). \
  load(basePath). \
  sort(["_hoodie_commit_time"]). \
  createOrReplaceTempView("hudi_trips_snapshot")

# 读取视图
result = spark.sql("select * from hudi_trips_snapshot")
print("-------------------------------------------start---------------------------------------------")
result.show()
print("-------------------------------------------stop----------------------------------------------")