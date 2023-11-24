from typing import Callable, TypeVar

InstanceType = TypeVar("InstanceType")

class ClientCache:
	clients: dict = {}

	def __init__(self):
		self.clients = {}

	@classmethod
	def load(cls, property: str, callback: Callable[..., InstanceType], *args, **kwargs) -> InstanceType:
		if not (property in cls.clients):
			instance = callback(*args, **kwargs)
			cls.clients[property] = instance
		return cls.clients[property]
	
class CloudClientManager:

	@classmethod
	@property
	def firestore(cls):
		from google.cloud.firestore import Client
		return ClientCache.load("firestore", Client)
	
	@classmethod
	@property
	def bigquery(cls):
		from google.cloud.bigquery import Client
		return ClientCache.load("bigquery", Client)
	
	@classmethod
	@property
	def pubsub(cls):
		from google.cloud.pubsub import PublisherClient
		return ClientCache.load("pubsub", PublisherClient)
