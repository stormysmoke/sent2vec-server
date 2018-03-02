#!/usr/bin/env python
"""
A client program for testing the Sent2Vec backend.

Usage:
    client.py index [-t <text>]
    client.py query [-s <sentence>] [-i <id>] [-k <int>]

Options:
    -t <text>      The text to index
    -s <sentence>  The query sentence
    -i <id>        The record ID on which to perform the query
    -k <int>       The number of nearest neighbours to return

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
index_t = "In this tutorial, the learning speed is your choice. Everything is up to you. If you are struggling, take a break, or reread the material."
query_s = "If you have problems, do a pause."
query_i = "123abc"
query_k = 3

class RpcClient(object):
    """
    A client for the Sent2Vec service for testing.
    """

    req_queue_name = "website-to-sent2vec"

    def __init__(self):
        """
        Create an RPC client for single-argument RPC calls.
        """
        # If RabbitMQ server URI defined in an env variable, use it
        var_name = 'RABBITMQ_URI'
        if var_name in os.environ:
            rabbitmq_uri = os.environ[var_name]
            print("Connecting to RabbitMQ on " + rabbitmq_uri)
            self.connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
        # If no RabbitMQ server URI, connect to RabbitMQ server on localhost
        else:
            print("No RABBITMQ_URI env variable found, connecting to RabbitMQ on localhost.")
            self.connection = pika.BlockingConnection()

        self.channel = self.connection.channel()

        # Queue for requests from client to server
        self.req_queue = self.channel.queue_declare(self.req_queue_name)

        # Queue for responses from server (auto-named)
        self.res_queue = self.channel.queue_declare(exclusive=True).method.queue

        # Register callback method for handling messages in response queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.res_queue)


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
if args['index']:
    t = args['-t'] if args['-t'] != None else index_t
    req = json.dumps(dict(method = "index", params = t))
else:
    s = args['-s'] if args['-s'] != None else query_s
    i = args['-i'] if args['-i'] != None else query_i
    k = args['-k'] if args['-k'] != None else query_k
    req = json.dumps(dict(method = "query", params = [s, int(k)]))

print(" [x] Sending: %s" % req)
res = client.call(req)
print(" [.] Receiving: %s" % res)

