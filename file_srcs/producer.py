from datetime import datetime
import os
import time

import requests
from kafka import KafkaProducer
import logging
import json
import jsbeautifier
import random


def produce() -> None:
    topic = 'TOPIC'

    # uncomment to enable more verbose kafka logging
    logging.basicConfig(level=logging.DEBUG)

    bootstrap_server = '50.19.186.89'
    kafka_port = '9092'

    # acquire the producer
    producer = KafkaProducer(
        bootstrap_servers=[f'{bootstrap_server}:{kafka_port}'])

    loop_based: bool = False

    data = batch_call_data() if loop_based else multi_call_data()

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
    # global app_id, api_key, base_url, endpoint, request_url, url_options
    loop_count = 0
    data = []
    for _ in range(0, loop_count):
        # next comment is a synchronization point, to be leveraged by ansible
        # insert loop logic here
        endpoint_suffix = 'endpoint_suffix'
        response = requests.get(build_url(endpoint_suffix))  # (request_url)
        if response:
            timestamp = datetime.timestamp(datetime.utcnow())
            response['timestamp'] = timestamp
            data.append(response)

    return data


def batch_call_data() -> list:
    # global app_id, api_key, base_url, data_index, endpoint, request_url, url_options
    endpoint_suffix = 'endpoint_suffix'
    response = requests.get(build_url(endpoint_suffix))  # (request_url)

    data = response.json()[data_index] if response else []

    for datum in data:
        # timestamp event was sent
        timestamp = datetime.timestamp(datetime.utcnow())
        datum['timestamp'] = timestamp

    return data


def build_url(endpoint_suffix: str) -> str:
    app_id = 'APP_ID'
    api_key = 'API_KEY'
    base_url = 'api_url'
    data_index = 'DATA_INDEX'
    endpoint = 'api_endpoint'
    url_options = 'url_options'
    return f'{base_url}{endpoint}{endpoint_suffix}?{url_options}'


if __name__ == '__main__':
    produce()
