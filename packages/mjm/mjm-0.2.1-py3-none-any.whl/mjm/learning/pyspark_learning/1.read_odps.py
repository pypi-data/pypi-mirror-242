from pyspark.sql import SparkSession
if __name__ == '__main__':
    spark = SparkSession.builder.appName("spark sql").config("spark.hadoop.fs.defaultFS","file:///").enableHiveSupport().getOrCreate()
    df = spark.sql("select * from lebo_data.base_sdk_channel")
    df.show()
    # spark = SparkSession.builder \
    # .appName("Python Spark OSS") \
    # .getOrCreate()
    # dataframe = spark.read.csv('https://big-oss.oss-cn-shenzhen.aliyuncs.com/223.119.31ip%E5%BC%80%E5%A4%B4%E7%9A%84%E8%BF%913%E4%B8%AA%E6%9C%88%E7%9A%84%E6%95%B0%E6%8D%AE.csv', header=True, inferSchema=True)
    # dataframe.show()
    # spark = SparkSession.builder.appName("Python Spark SQL OSS example").getOrCreate()
    # pathIn = "oss://bucket/path/to/read"
    # df = spark.read.text(pathIn)
    # cnt = df.count()
    # print(cnt)
    # outputPath = "oss://bucket/path/to/write"
    # df.write.format("parquet").mode('overwrite').save(outputPath)
    # dataframe = spark.read.csv('https://big-oss.oss-cn-shenzhen.aliyuncs.com/223.119.31ip%E5%BC%80%E5%A4%B4%E7%9A%84%E8%BF%913%E4%B8%AA%E6%9C%88%E7%9A%84%E6%95%B0%E6%8D%AE.csv', header=True, inferSchema=True)
    # dataframe.show()

