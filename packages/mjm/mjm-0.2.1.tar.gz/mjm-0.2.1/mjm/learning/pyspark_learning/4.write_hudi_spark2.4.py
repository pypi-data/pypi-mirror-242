from pyspark.sql import SparkSession
# spark.serializer要在创建builder的时候就配置否则报错
spark = SparkSession.builder.appName('testoss').config("spark.serializer", "org.apache.spark.serializer.KryoSerializer").config('spark.sql.hive.convertMetastoreParquet','false').getOrCreate()
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
tableName = "hudi_trips_cow"
basePath = "oss://big-oss/tmp_mjm/huditest"
dataGen = sc._jvm.org.apache.hudi.QuickstartUtils.DataGenerator()
inserts = sc._jvm.org.apache.hudi.QuickstartUtils.convertToStringList(dataGen.generateInserts(10))
df = spark.read.json(spark.sparkContext.parallelize(inserts, 2))
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