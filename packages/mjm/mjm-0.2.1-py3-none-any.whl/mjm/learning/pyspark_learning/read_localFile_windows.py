#!/user/bin env python
# author:Simple-Sir
# create_time: 2022/6/6 14:20
from pyspark import SparkConf,SparkContext

sparkConf = SparkConf().setMaster("local[*]").setAppName("wc")
sc = SparkContext.getOrCreate(sparkConf)
# sc = SparkContext(master="local[*]",appName="wc")

# 创建RDD
rdd = sc.parallelize([1,2,3,4,5]) # 创建RDD
# print(rdd.getNumPartitions()) # 查看分区数 8
# print(rdd.repartition(2).glom().collect()) # 按照分区打印数据 [[2, 4], [1, 3, 5]]

# 读取文件构建RDD
rdd0 = sc.textFile("file:///D:\\workspace_python\\my_utils\\test\\wordcount.txt")
# print(rdd0.getNumPartitions()) # 查看分区数 2
# print(rdd0.repartition(2).glom().collect()) # 按照分区打印数据 [['hello world', 'hello python'], ['hello spark']]

# 统计
rdd0.flatMap(lambda x:x.split(" ")).map(lambda x:(x,1)).reduceByKey(lambda x,y:x+y).foreach(print)

sc.stop()