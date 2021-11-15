from datetime import datetime
import os
import time

import requests
from kafka import KafkaProducer
import logging
import json
import jsbeautifier


# topic to produce:
topic = 'TOPIC'

# uncomment to enable more verbose kafka logging
# logging.basicConfig(level=logging.DEBUG)

bootstrap_server = '50.19.186.89'
kafka_port = '9092'

# acquire the producer
producer = KafkaProducer(bootstrap_servers=[f'{bootstrap_server}:{kafka_port}'])

app_id = 'APP_ID'
api_key = 'API_KEY'
base_url = 'api_url'
endpoint = 'api_endpoint'
url_options = 'url_options'

request_url = f'{base_url}{endpoint}{url_options}'
response = requests.get(request_url)

if response:
    content = response.json()

    # get list of news stories
    data: list = content['data']

    beautifier_opts = jsbeautifier.default_options()
    beautifier_opts.indent_size = 2

    for datum in data:
        # timestamp event was sent
        timestamp = datetime.timestamp(datetime.utcnow())
        datum['timestamp'] = timestamp
        datum_content = json.dumps(datum)
        print(jsbeautifier.beautify(datum_content, beautifier_opts))
        producer.send(topic, value=bytes(datum_content, 'ascii'))
        producer.flush()
        time.sleep(1)

# we are done
producer.close()
