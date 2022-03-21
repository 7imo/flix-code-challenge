import json
from dateutil.parser import isoparse
from dateutil.tz import UTC
from kafka import KafkaConsumer
from kafka import KafkaProducer

INPUT_TOPIC = 'input_topic'
OUTPUT_TOPIC = 'output_topic'
BOOTSTRAP_SERVERS = ['kafka:9092']

def read_messages_from_topic(topic):

    # read msgs from topic
    consumer = KafkaConsumer(topic, 
                            bootstrap_servers=BOOTSTRAP_SERVERS,
                            value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    for msg in consumer:
        data = msg.value

        # convert ts to utc
        utc_ts = msg_timestamp_to_utc(data['myTimestamp'])

        # replace ts
        data['myTimestamp'] = utc_ts

        # write msg to output_topic
        write_message_to_topic(OUTPUT_TOPIC, json.dumps(data).encode('utf-8'))


def msg_timestamp_to_utc(ts):
    
    if not ts:
        # empty ts
        return ts
    else:
        # convert to utc and return string
        datetime = isoparse(ts)
        utc_ts = datetime.astimezone(UTC).isoformat()
        return str(utc_ts)


def write_message_to_topic(topic, msg):

    # publish new msg with correct ts
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    producer.send(topic, msg)


if __name__ == "__main__":
    read_messages_from_topic(INPUT_TOPIC)