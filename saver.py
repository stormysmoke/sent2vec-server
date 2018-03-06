import os
import uuid
import boto3
import tempfile
import serializer as s

def put(id, sent_arr, vec_arr):
    """
    Save an array of sentences and an array of vectors under the provided ID.

    Arguments:
        id:        a string ID
        sent_arr:  a NumPy array of unicode objects
        sent_vec:  a NumPy array of float vectors

    Return:
        Nothing.
    """
    sent_file = s.serialize_sent(sent_arr)
    _bucket().upload_file(sent_file, _s3_key_sent(id))
    os.remove(sent_file) 

    vec_file = s.serialize_vec(vec_arr)
    _bucket().upload_file(vec_file, _s3_key_vec(id))
    os.remove(vec_file)
    
def get(id):
    """
    Retrieve the sentence and vector array associated with the provided ID.

    Arguments:
        id:  a string ID that was previously used with put()

    Return:
        A dictionary with the keys 'sent' and 'vec' holding a NumPy arrays of
        sentences (as unicode objects) and a NumPy array of float vectors,
        respectively.
    """
    sent_file = _get_tmpfilename()
    _bucket().download_file(_s3_key_sent(id), sent_file)
    sent_arr = s.deserialize_sent(sent_file)
    os.remove(sent_file)

    vec_file = _get_tmpfilename()
    _bucket().download_file(_s3_key_vec(id), vec_file)
    vec_arr = s.deserialize_vec(vec_file)
    os.remove(vec_file)
   
    return dict(sent=sent_arr, vec=vec_arr)

def _bucket():
    """
    Get a handle to the S3 bucket where the objects are stored.
    """
    return boto3.resource('s3').Bucket('stormysmoke-sent2vec')

def _s3_key_sent(id):
    """
    Given an ID, return the key name for a "sent" object stored on S3.
    """
    return id + '/sent' + s.get_filename_ext_sent()


def _s3_key_vec(id):
    """
    Given an ID, return the key name for a "vec" object stored on S3.
    """
    return id + '/vec' + s.get_filename_ext_vec()

def _get_tmpfilename():
    """
    Get a sufficiently unique filename in the system's temp directory.
    """
    return tempfile.gettempdir() + '/' + str(uuid.uuid4())
