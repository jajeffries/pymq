
from unittest import TestCase
from unittest import main as run_tests

from mq import *

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