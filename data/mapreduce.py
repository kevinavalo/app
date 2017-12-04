from pyspark import SparkContext
import MySQLdb
import time


db = MySQLdb.connect(host='db', user='www', passwd='$3cureUS', db='cs4501')
cur = db.cursor()
while True:
	cur.execute('delete from ItemManager_recommendation')

	sc = SparkContext("spark://spark-master:7077", "PopularItems")

	data = sc.textFile("/tmp/data/recommendations.log", 2)     # each worker loads a piece of the data file

	pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

	pairs2 = pairs.groupByKey()   # (User,list of item ids)
	# pairs3 = pairs2.map(lambda pair: (pair[0], pair[1].distinct()))

	cartesian = []
	for user, items in pairs2.collect():
		product = sc.parallelize(items).cartesian(sc.parallelize(items)).filter(lambda x: x[0] != x[1]).distinct()
		for c in product.collect():
			t = (user,c)
			cartesian.append(t)

	cartesian = sc.parallelize(cartesian)


	pages = cartesian.map(lambda pair: (pair[1], pair[0]))

	output = {}
	for tup, peeps in pages.groupByKey().collect():
		tup = tuple(tup)
		output[tup] = len(peeps)

	recom_dict = {}
	for page, count in output.items():
		if count >= 3:
			try:
				recom_dict[page[0]] += ' '+str(page[1])
			except KeyError as e:
				recom_dict[page[0]] = str(page[1])


	for key, value in recom_dict.items():
		val = value.encode('UTF-8')
		k = int(key)
		query = 'INSERT INTO ItemManager_recommendation (item_id, recommended_items) VALUES (%d, \'%s\');' % (k, val)
		cur.execute(query)
		print(key, value, 'inserted?')

	db.commit()

	time.sleep(120)
	sc.stop()

