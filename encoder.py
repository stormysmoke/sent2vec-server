import json

"""
Network communication message format.

This implementation: JSON RPC 2.0 with named parameters in the request objects.
"""

def decode_request(body):
    """
    Decode a request message to a dictionary containig the request information.

    Arguments:
        body:  the body of a message as received over the wire

    Returns:
        A dictionary with the two keys 'method' and 'params'. The following two
        combination of values are possible:
            - {method='encode', params={text=<str>}}
            - {method='knn', params={query=<str>, k=<int>, id=<str>}}
    """
    j = json.loads(body)

    if not 'method' in j or not 'params' in j:
        raise Exception("Invalid message: " + body)

    if j['method'] == 'encode':
        if not 'text' in j['params']:
            raise Exception(_missing_param('text', body))
        method = 'encode'
        params = dict(text=j['params']['text'])

    elif j['method'] == 'knn':
        if not 'query' in j['params']:
            raise Exception(_missing_param('query', body))
        if not 'k' in j['params']:
            raise Exception(_missing_param('k', body))
        if not 'id' in j['params']:
            raise Exception(_missing_param('id', body))
        method = 'knn'
        p = j['params']
        params = dict(query=p['query'], k=p['k'], id=p['id'])

    else:
        raise Exception("Invalid request method: " + j['method'])

    return dict(method=method, params=params)

def encode_response(obj):
    """
    Encode a response object to a message body to be sent over the wire.

    Arguments:
        obj:  any type of object

    Returns:
        An appropriately encoded message body to be sent over the wire.
    """
    return json.dumps(dict(result=obj))

def _missing_param(p, body):
    return "Param '%s' missing in: %s" % (p, body)
