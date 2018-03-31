import os
import pika
import encoder

"""
Network communication with the client.

This implemenation uses RabbitMQ as a message broker.
"""

_req_queue = 'sent2vec-client-to-server'
_var = 'RABBITMQ_URI'

_channel = None
_on_encode = None
_on_knn = None

def _on_request(channel, method, props, body):
    """
    Callback function called whenever a message is consumed from the queue.
    """
    # Decode and handle request
    print(" [x] Receiving: " + body)
    decoded = encoder.decode_request(body)
    if decoded['method'] == 'encode':
        result = _on_encode(decoded['params']['text'])
    elif decoded['method'] == 'knn':
        p = decoded['params']
        result = _on_knn(p['query'], p['k'], p['id'])
    # Encode and return response
    response = encoder.encode_response(result, body)
    print(" [ ] Returning: " + response)
    channel.basic_publish(exchange='', routing_key=props.reply_to, body=response);
    channel.basic_ack(delivery_tag=method.delivery_tag)

def init():
    """
    Set up any required network communication connections.
    """
    global _channel
    uri = os.environ[_var] if _var in os.environ else 'amqp://guest:guest@localhost:5672/'
    print("Connecting to RabbitMQ: " + uri)
    connection = pika.BlockingConnection(pika.URLParameters(uri))
    _channel = connection.channel()
    _channel.queue_declare(_req_queue, auto_delete=True)
    _channel.basic_qos(prefetch_count=1)
    _channel.basic_consume(_on_request, queue=_req_queue)

def register_on_encode(fun):
    """
    Register function to be called when an "encode" request is received.

    Arguments:
        fun:  a function taking the following arguments:
                text:  the text to be encoded
    """
    global _on_encode
    _on_encode = fun

def register_on_knn(fun):
    """
    Register function to be called when a "knn" request is received.

    Arguments:
        fun:  a function taking the following arguments:
                query:  the query sentence
                k:      number of nearest neighbours to return
                id:     ID of the encoded text to which to apply the query
    """
    global _on_knn
    _on_knn = fun

def start_listening():
    """
    Start listening for requests from the client.

    This function must be called after the "init" and "register_..." functions.
    This call is blocking!
    """
    print(" [X] Awaiting RPC requests")
    _channel.start_consuming()
