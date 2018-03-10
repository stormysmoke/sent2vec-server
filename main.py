import communicator
import sent2vec
import saver
import uuid

"""
Highest-level module and entry point to the application.
"""

def _on_encode(text):
    record = sent2vec.encode(text)
    id = str(uuid.uuid4())
    saver.put(id, record['sent'], record['vec'])
    return id

def _on_knn(query, k, id):
    record = saver.get(id)
    return sent2vec.knn(query, record, k)

sent2vec.init()
communicator.init()
communicator.register_on_encode(_on_encode)
communicator.register_on_knn(_on_knn)

# This call is blocking and must come last
communicator.start_listening()
