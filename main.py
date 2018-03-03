#!/usr/bin/env python

import os
import pika
import json
import sent2vec_manager

rabbitmq_queue = "sent2vec-front-to-back"

# Callback function for handling message in the request queue
def __on_request(channel, method, props, body):

    # Decode request from JSON message
    request = json.loads(body)

    print(" [.] Receiving " + str(request))

    # Request is to index a piece of text
    if request['method'] == "index":
        text = request['params']
        id = sent2vec_manager.index_string(text)
        result = id
    # Request is to query a sentence in a previously indexed piece of text
    elif request['method'] == "query":
        sentence = request['params'][0]
        k = request['params'][1]
        result = sent2vec_manager.query(sentence, int(k))
    else:
        raise Exception("Invalid method: " + request['method'])

    # Encode response to JSON message
    response = dict(result=result)

    print(" [ ] Returning" + str(response))

    response_props = pika.BasicProperties(correlation_id=props.correlation_id)
    channel.basic_publish(exchange='',
                          routing_key=props.reply_to,
                          properties=response_props,
                          body=json.dumps(response))

    channel.basic_ack(delivery_tag=method.delivery_tag)

# If there is a RabbitMQ server URI defined in an env variable, use it
var_name = 'RABBITMQ_URI'
if var_name in os.environ:
    rabbitmq_uri = os.environ[var_name]
    print("Connecting to RabbitMQ: " + rabbitmq_uri)
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_uri))
# If there is no RabbitMQ server URI, connect to RabbitMQ server on localhost
else:
    print("Connecting to default RabbitMQ server on localhost.")
    connection = pika.BlockingConnection()

# Establish connection to RabbitMQ server
channel = connection.channel()

# Queue for requests from the website to sent2vec server
req_queue = channel.queue_declare(rabbitmq_queue)

# Register callback function for handling messages in request queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(__on_request, queue=rabbitmq_queue)

# Initialise the Sent2Vec encoder
sent2vec_manager.init()

# Wait for and handle RPC requests
print(" [x] Awaiting RPC requests")
channel.start_consuming()