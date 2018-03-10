import os
import pika
import json

_queue = 'sent2vec-front-to-back'
_var = 'RABBITMQ_URI'

_channel = None
_on_encode = None
_on_knn = None

def _on_request(channel, method, props, body):
    req = json.loads(body)
    print(" [.] Receiving " + str(req))
    params = req['params']
    if req['method'] == 'encode':
        result = _on_encode(params['text'])
    elif req['method'] == 'knn':
        result = _on_knn(params['query'], params['k'], params['id'])
    else:
        raise Exception("Invalid request method: " + req['method'])
    response = json.dumps(dict(result=result))
    print(" [ ] Returning" + str(response))
    channel.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response)
    channel.basic_ack(delivery_tag=method.delivery_tag)

def init():
    global _channel
    uri = os.environ[_var] if _var in os.environ else 'amqp://guest:guest@localhost:5672/'
    print("Connecting to RabbitMQ: " + uri)
    connection = pika.BlockingConnection(pika.URLParameters(uri))
    _channel = connection.channel()
    _channel.queue_declare(_queue)
    _channel.basic_qos(prefetch_count=1)
    _channel.basic_consume(_on_request, queue=_queue)

def register_on_encode(fun):
    global _on_encode
    _on_encode = fun

def register_on_knn(fun):
    global _on_knn
    _on_knn = fun

def start_listening():
    print(" [x] Awaiting RPC requests")
    _channel.start_consuming()
