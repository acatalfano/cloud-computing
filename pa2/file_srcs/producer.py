from datetime import datetime
import os
import time

import requests
from kafka import KafkaProducer
import logging
import json
import jsbeautifier
import random
import pprint


def produce() -> None:
    topic = 'TOPIC'

    # uncomment to enable more verbose kafka logging
    logging.basicConfig(level=logging.DEBUG)

    bootstrap_server = '50.19.186.89'
    kafka_port = '9092'

    # acquire the producer
    producer = KafkaProducer(
        bootstrap_servers=[f'{bootstrap_server}:{kafka_port}'])

    batch_call: bool = False

    data = batch_call_data() if batch_call else multi_call_data()

    beautifier_opts = jsbeautifier.default_options()
    beautifier_opts.indent_size = 2

    for datum in data:
        datum_content = json.dumps(datum)
        print(jsbeautifier.beautify(datum_content, beautifier_opts))
        producer.send(topic, value=bytes(datum_content, 'ascii'))
        producer.flush()
        time.sleep(1)

    # we are done
    producer.close()


def multi_call_data() -> list:
    loop_count = 10
    data = []
    for _ in range(0, loop_count):
        # next comment is a synchronization point, to be leveraged by ansible
        # insert loop logic here
        endpoint_suffix = 'endpoint_suffix'
        response = requests.get(build_url(endpoint_suffix))
        if valid_status_code(response):
            datum = response.json()
            timestamp = datetime.timestamp(datetime.utcnow())
            datum['timestamp'] = timestamp
            data.append(datum)

    return data


def batch_call_data() -> list:
    endpoint_suffix = 'endpoint_suffix'
    data_index = 'DATA_INDEX'
    response = requests.get(build_url(endpoint_suffix))

    data = response.json()[data_index] if valid_status_code(response) else []

    for datum in data:
        # timestamp event was sent
        timestamp = datetime.timestamp(datetime.utcnow())
        datum['timestamp'] = timestamp

    return data


def build_url(endpoint_suffix: str) -> str:
    app_id = 'APP_ID'
    api_key = 'API_KEY'
    base_url = 'api_url'
    endpoint = 'api_endpoint'
    url_options = 'url_options'
    return f'{base_url}{endpoint}{endpoint_suffix}?{url_options}'


def valid_status_code(response: requests.Response) -> bool:
    return bool(response) and response.status_code >= 200 and response.status_code < 300


if __name__ == '__main__':
    produce()
