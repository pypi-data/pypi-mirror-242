import json
from .cloud_client_manager import CloudClientManager

def publish_to_topic(project: str, topic: str, attributes: dict) -> None:

	publisher = CloudClientManager.pubsub

	topic_name = f'projects/{project}/topics/{topic}'

	print(f"Publishing to [{topic_name=}] with", attributes)

	message_data = json.dumps(attributes)
	message_data_bytes = message_data.encode()

	publisher.publish(topic_name, data=message_data_bytes)