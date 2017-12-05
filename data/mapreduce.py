from pyspark import SparkContext
import itertools
import MySQLdb
import time

def create_pairs(user, items):
	item_pairs = list(itertools.combinations(items, 2))
	all_pairs = []
	for item in item_pairs:
		all_pairs.append((user, item))
	return all_pairs

db = MySQLdb.connect(host='db', user='www', passwd='$3cureUS', db='cs4501')
cur = db.cursor()
while True:
	cur.execute('delete from ItemManager_recommendation')

	sc = SparkContext("spark://spark-master:7077", "PopularItems")

	data = sc.textFile("/tmp/data/recommendations.log", 2)     # each worker loads a piece of the data file

	pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

	pairs2 = pairs.groupByKey().mapValues(list)   # (User,list of item ids) groupByKey().mapValues(list)
	# pairs3 = pairs2.map(lambda pair: (pair[0], pair[1].distinct()))
	print("pairs2----------:", pairs2.collect())

	pairs3 = pairs2.flatMap(lambda pair: create_pairs(pair[0], pair[1]))
	pairs3 = pairs3.distinct()

	print("pairs3---------:", pairs3.collect())


	pairs4 = pairs3.map(lambda pair: (pair[1], pair[0]))

	pairs4 = pairs4.groupByKey().mapValues(list)

	print("pairs4-------------:", pairs4.collect())

	pairs5 = pairs4.map(lambda pair: (pair[0], len(pair[1])))

	print("pairs5-------------:", pairs5.collect())


	pairs6 = pairs5.filter(lambda pair: pair[1] > 2)

	print("pairs6------------:", pairs6.collect())


	# pages = cartesian.map(lambda pair: (pair[1], pair[0]))

	output = pairs6.collect()

	recom_dict = {}
	for page, count in output:
		print("page_-------------:", page)
		print("count-------------:", count)
		if count >= 3:
			try:
				if str(page[1]) not in recom_dict[page[0]] and str(page[0]) != str(page[1]): 
					recom_dict[page[0]] += ' '+str(page[1])
				if str(page[0]) not in recom_dict[page[1]] and str(page[0]) != str(page[1]):
					recom_dict[page[1]] += ' '+str(page[0])
			except KeyError as e:
				recom_dict[page[0]] = str(page[1])
				recom_dict[page[1]] = str(page[0])

	print("recom_dict--------------:", recom_dict)
	to_write = ''
	for key, value in recom_dict.items():
		print("HELLO I LOVE KEV------------------------------------------------------------------")
		val = value.encode('UTF-8')
		query = 'INSERT INTO ItemManager_recommendation (item_id, recommended_items) VALUES (%d, \'%s\');' % (int(key), val)
		cur.execute(query)
		to_write += (key + '\t' + val + '\n')
	
	with open("/tmp/data/output.log","w") as f:
		f.write(to_write)
		f.close()

	db.commit()

	sc.stop()
	time.sleep(120)

