# -*- coding: utf-8 -*-
import sys
from pyspark.sql import SparkSession

try:
    # for python 2
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    # python 3 not needed
    pass

if __name__ == '__main__':
    spark = SparkSession.builder\
        .appName("spark write df to oss")\
        .getOrCreate()

    data = [i for i in range(0, 100)]

    df = spark.sparkContext.parallelize(data, 2).map(lambda s: ("name-%s" % s, s)).toDF("name: string, num: int")

    df.show(n=10)

    # write to oss
    pathout = 'oss://big-oss/tmp_mjm/test.csv'
    df.write.csv(pathout)