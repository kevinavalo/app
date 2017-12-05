import time
import json
from kafka import KafkaConsumer

consumer = None
while consumer == None:
	try:
		consumer = KafkaConsumer('recommendation-topic', group_id='listing-recs', bootstrap_servers=['kafka:9092'])
	except:
		time.sleep(1)

for message in consumer:
	body = json.loads((message.value).decode('utf-8'))
	with open("/app2/recommendations.txt","a") as rec:
		# print("Hey I got here")
		# rec.write('HELLO')
		rec.write(body['username'] + '\t' + body['item_id'] + '\n')
		rec.close()



# 	es.index(index='listing_index', doc_type='listing', id=body['id'], body=body)
# 	es.indices.refresh(index="listing_index")