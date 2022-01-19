import pyspark 
from pyspark.sql import SparkSession 

spark = SparkSession
    .builder
    .appName("PythonWordCount")
    .getOrCreate()

lines = spark.read.text(sys.argv[1]).rdd.map(lambda r:r[0])

counts = lines.flatMap(lambda x:split(''))
    .map(lambda x: (x,1))
    .reduceByKey(add)

outputs = counts.collect()

for(word, count) in outputs:
    print("%s: %i" % (word, count))

spark.stop()
