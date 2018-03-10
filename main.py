import communicator
import sent2vec
import saver
import uuid

def on_encode(text):
    record = sent2vec.encode(text)
    id = str(uuid.uuid4())
    saver.put(id, record['sent'], record['vec'])
    return id

def on_knn(query, k, id):
    record = saver.get(id)
    res = sent2vec.knn(query, record['vec'], k)
    return dict(sent=record['sent'][res['i']].tolist(), dist=res['dist'])

sent2vec.init()
communicator.init()
communicator.register_on_encode(on_encode)
communicator.register_on_knn(on_knn)

# This call is blocking and must come last
communicator.start_listening()
