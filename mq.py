
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

from flask import Flask, request
from json import dumps as to_json
from json import loads as from_json

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
SUCCESS = ""

subscriptions = Subscriptions()

@app.route("/queues")
def get_all_queue_names():
	return to_json(subscriptions.queues.keys()), 200

@app.route("/queues/<queue>", methods = ['POST'])
def create_queue(queue):
	subscriptions.add_queue(InMemoryQueue(queue))
	return "", 200

@app.route("/queues/<queue>/subscriptions", methods = ['POST'])
def subscribe(queue):
	request_body = from_json(request.data)
	if(queue in subscriptions.queues):
		# the callback here should be a partially applied function which calls the uri
		subscriptions.subscribe(queue, request_body['callback'])
		return SUCCESS
	else:
		return "Queue not found", 400 

@app.route("/queues/<queue>/message", methods = ['POST'])
def subscribe(queue):
	if(queue in subscriptions.queues):
		subscriptions.queues[queue].post(request.data)
		return SUCCESS
	else:
		return "Queue not found", 400 

if __name__ == '__main__':
    app.run()