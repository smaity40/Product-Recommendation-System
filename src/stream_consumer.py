from kafka import KafkaConsumer
import json
from inference import recommend

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='recommendation-group'
)

print("📡 Listening for events...")
for msg in consumer:
    event = msg.value
    print(f"\n👤 Event Received: {event}")
    
    result = recommend(event['user_id'], event.get('top_k', 5))

    # Ensure result is a dictionary
    if isinstance(result, dict) and "recommendations" in result:
        print("🔎 Recommended Products:")
        for r in result["recommendations"]:
            print(f" - {r['product_id']} → {r['product_name']}")
    else:
        print("⚠️ Recommendation failed or returned invalid format:", result)
