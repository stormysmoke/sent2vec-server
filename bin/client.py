#!/usr/bin/env python
"""
A client program for testing the Sent2Vec server.

Usage:
    client.py encode [-t <text>]
    client.py knn [-q <query>] [-k <int>] [-i <id>]

Options:
    -t <text>   The text to encode
    -q <query>  The query sentence
    -k <int>    The number of nearest neighbours to return
    -i <id>     The record ID on which to perform the query

Note: if any of the options is omitted, then a default value is used (see code
for details).
"""

import os
import sys
import pika
import uuid
import json
from docopt import docopt

# Parse command-line args with docopt
args = docopt(__doc__)

# Default values for command-line options
encode_t = "In this tutorial, the learning speed is your choice. Everything is up to you. If you are struggling, take a break, or reread the material."
knn_q = "If you have problems, do a pause."
knn_i = "123abc"
knn_k = 3

class RpcClient(object):
    """
    A client for the Sent2Vec service for testing.
    """

    req_queue_name = "sent2vec-front-to-back"

    def __init__(self):
        """
        Create an RPC client for single-argument RPC calls.
        """
        if 'RABBITMQ_URI' in os.environ:
            uri = os.environ['RABBITMQ_URI']
        else:
            uri = 'amqp://guest:guest@localhost:5672/'
        print("Connecting to RabbitMQ: " + uri)
        self.connection = pika.BlockingConnection(pika.URLParameters(uri))
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.req_queue_name)
        self.res_queue = self.channel.queue_declare(exclusive=True).method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.res_queue)

    def on_response(self, channel, method, props, body):
        """
        Callback method handling messages in the response queue.
        """
        if self.correlation_id == props.correlation_id:
            self.response = body


    def call(self, arg):
        """
        Perform RPC call with a single argument.
        """
        # Note: it's safe to use instance variables for response and corr ID,
        # because the RPC client object can perform only a single RPC call at
        # (a new call can only be performed when the previous one finished).
        self.response = None
        self.correlation_id = str(uuid.uuid4())

        # Send message to server
        props = pika.BasicProperties(reply_to=self.res_queue,
                                     correlation_id=self.correlation_id)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.req_queue_name,
                                   properties=props,
                                   body=str(arg))

        # Block until the response message has been read from response queue
        while self.response is None:
            self.connection.process_data_events()

        return self.response

# Main program
client = RpcClient()

req = ""
if args['encode']:
    t = args['-t'] if args['-t'] != None else encode_t
    params = dict(text=t)
    req = json.dumps(dict(method='encode', params=params))
elif args['knn']:
    q = args['-q'] if args['-q'] != None else knn_q
    i = args['-i'] if args['-i'] != None else knn_i
    k = args['-k'] if args['-k'] != None else knn_k
    params = dict(query=q, k=k, id=i)
    req = json.dumps(dict(method = "knn", params=params))

print(" [x] Sending: %s" % req)
res = client.call(req)
print(" [.] Receiving: %s" % res)

