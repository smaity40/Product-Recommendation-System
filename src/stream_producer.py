from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event = {
    "user_id": "AG3D6O4STAQKAY2UVGEUV46KN35Q",
    "top_k": 5
}

producer.send("user-events", event)
producer.flush()
print("✅ Event sent to Kafka!")
