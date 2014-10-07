
class Subscriptions(object):
	def __init__(self):
		self.queues = {}

	def subscribe(self, queue_name, callback):
		self.queues[queue_name].add_subscriber(callback)

	def add_queue(self, queue):
		self.queues[queue.name] = queue

class InMemoryQueue(object):

	def __init__(self, name):
		self.name = name
		self._callbacks = []

	def add_subscriber(self, callback):
		self._callbacks.append(callback)

	def post(self, message):
		for callback in self._callbacks:
			callback(message)


from unittest import TestCase
from unittest import main as run_tests

class TestMe(TestCase):
	
	def test_can_subscribe_to_queue(self):
		message = "hi!"
		self.message_recieved = None
		def callback(message):
			self.message_recieved = message
		sub = Subscriptions()
		queue = InMemoryQueue("My Queue")
		sub.add_queue(queue)
		sub.subscribe("My Queue", callback)
		queue.post(message)
		self.assertEqual(self.message_recieved, message)

if __name__ == "__main__":
	run_tests()