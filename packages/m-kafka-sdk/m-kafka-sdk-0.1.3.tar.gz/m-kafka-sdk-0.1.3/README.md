- **Thư viện Consumer của Profiling** :
* Tự động tạo kafka topics
```python
from mobio.libs.kafka_lib.helpers.ensure_kafka_topic import create_kafka_topics
create_kafka_topics(['test1'])
```

* Confluent Kafka Consumer

```python
import os
from mobio.libs.kafka_lib import ConsumerGroup
from pymongo import MongoClient 
from mobio.libs.kafka_lib.helpers.confulent_consumer_manager import ConfluentConsumerManager, ConfluentMessageQueue

# Đây là function khởi tạo client-mongo
def create_db():
    print("create_db: ok")

    try:
        url_connection = os.getenv('MONGODB_URI')
        client = MongoClient(url_connection, connect=False)
    except Exception as ex:
        print('ERROR:: create_db: {}'.format(ex))
        client = None

    return client

class ConfluentKafkaConsumer(ConfluentMessageQueue):

    def __init__(self, mongo_client, topic_name, num_worker, group_id):
        super().__init__(mongo_client, topic_name, num_worker, group_id)

    def process_msg(self, payload):
        print("payload: {}".format(payload))
        raise Exception("test")

def start_confluent_consumer():
    mongo_client = create_db()
    consumer_list = [(ConfluentKafkaConsumer, mongo_client, 'test1', 1, ConsumerGroup.DEFAULT_CONSUMER_GROUP_ID, True)]

    if consumer_list:
        manager = ConfluentConsumerManager(consumer_list)


if __name__ == "__main__":
    # test_create_topic()
    # start_kafka_python()
    start_confluent_consumer()
```
        
* Update version 0.1.1
```text
support Enable/Disable retry consumer
```

* Update version 0.1.2
```text
add ConfluentProducerManager
```

* Update version 0.1.2
```text
add ConfluentProducerManager
```