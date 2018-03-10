import numpy
import json
import gzip
import tempfile
import uuid

"""
Converting arrays of sentences and vectors to files and vice versa.

This implementation uses the NPY format for vector arrays and gzip-compressed
JSON for sentence arrays.
"""

def get_filename_ext_sent():
    """
    Filename extension that clients may add to files created by serialize_sent
    in order to give an informal indication about the format of the file.
    """
    return '.json.gz'

def get_filename_ext_vec():
    """
    Filename extension that clients may add to files created by serialize_vec
    in order to give an informal indication about the format of the file.
    """
    return '.npy'

def serialize_sent(sent):
    """
    Convert an array of sentences (unicode objects) to a gzip-compressed JSON
    file. Unicode objects are encoded with UTF-8.

    Arguments:
        sent:  a NumPy array of unicode objects.

    Return:
        The absolute path name of the gzip-compressed JSON file.
    """
    path = _get_tmpfilename()
    with gzip.open(path, 'wb') as gzipfile:
        gzipfile.write(json.dumps(sent.tolist()))
    return path
    
def serialize_vec(vec):
    """
    Convert a NumPy array of numerical vectors to a NumPy (npy) file.

    Arguments:
        vec:  a two-dimensional NumPy array of floats.

    Return:
        The absolute path name of a NumPy (npy) file.
    """
    path = _get_tmpfilename()
    # Caution: don't use path as 1st arg for save, because it would add ".npy"
    with open(path, 'wb') as f:
        numpy.save(f, vec)
    return path

def deserialize_sent(path):
    """
    Convert a gzip-compressed JSON file, as produced by serialize_sent, back to
    a NumPy array of unicode objects.

    Arguments:
        path:  path to a gzip-compressed JSON file.

    Return:
        A NumPy array of unicode objects.
    """
    with gzip.open(path, 'rb') as gzipfile:
        content = gzipfile.read()
    return numpy.array(json.loads(content))

def deserialize_vec(path):
    """
    Convert a NumPy (npy) file, as produced by serialize_vec, to a NumPy array.

    Arguments:
        vec:  path to a NumPy (npy) file.

    Return:
        The NumPy array that was saved in the NumPy file.
    """
    return numpy.load(path)

def _get_tmpfilename():
    """
    Get a sufficiently unique filename in the system's temp directory.
    """
    return tempfile.gettempdir() + '/' + str(uuid.uuid4())
