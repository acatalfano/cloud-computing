from kafka import KafkaConsumer
from json import loads
from os import path
import couchdb
import jsbeautifier

topics = ['weather', 'news']

couch_db_ip = path.expandvars('$COUCH_DB_IP')
kafka_1_ip = path.expandvars('$KAFKA_1_IP')
kafka_2_ip = path.expandvars('$KAFKA_2_IP')
kafka_ips = [kafka_1_ip, kafka_2_ip]

couch_db_port = '5984'
kafka_port = '9092'

username = 'USERNAME'
password = 'PASSWORD'

couch = couchdb.Server(
    f'http://{username}:{password}@{couch_db_ip}:{couch_db_port}/')

beautifier_opts = jsbeautifier.default_options()
beautifier_opts.indent_size = 2


def try_get_db(db_name):
    try:
        db = couch[db_name]
    except:
        db = couch.create(db_name)
    return db


def write_to_db(msg):
    # print(msg.topic + ':')
    # print(jsbeautifier.beautify(msg.value.decode('utf-8'), beautifier_opts))
    # print(msg.topic + ':' + '\n' + msg.value + '\n\n')
    db_map[msg.topic].save(msg.value)
    # db = db_map[msg.topic]
    # content = msg.value
    # db.save(content)


topics = ['weather', 'news']
db_map = {topic: try_get_db(topic) for topic in topics}

consumer = KafkaConsumer(
    'weather', 'news',
    bootstrap_servers=list(map(lambda ip: f'{ip}:{kafka_port}', kafka_ips)),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='0',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

for message in consumer:
    write_to_db(message)
