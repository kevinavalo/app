from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/recommendations.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

pairs2 = pairs.groupByKey()   # (User,list of item ids)
# pairs3 = pairs2.map(lambda pair: (pair[0], pair[1].distinct()))

cartesian = []
for user, items in pairs2.collect():
	product = sc.parallelize(items).cartesian(sc.parallelize(items)).filter(lambda x: x[0] < x[1]).distinct()
	for c in product.collect():
		t = (user,c)
		cartesian.append(t)

print("cartesian %s" % cartesian)

cartesian = sc.parallelize(cartesian)


pages = cartesian.map(lambda pair: (pair[1], pair[0]))
for tup, peeps in pages.groupByKey().collect():
    for thing in peeps:
    	print ((tup, thing))
print ("Popular items done")



# print("pages", pages.groupByKey().collect())

# count = pages.reduceByKey(lambda x,y: int(x)+int(y))        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together

# output = count.collect()                          # bring the data back to the master node so we can print it out
# for page_id, count in output:
#     print ("page_id %s count %d" % (page_id, count))
# print ("Popular items done")

sc.stop()