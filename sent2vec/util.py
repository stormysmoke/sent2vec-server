"""
Various utility functions.
"""

def str2unicode(s):
    """Convert a string to a UTF-8 Unicode object."""
    return s.decode('utf-8')

def unicode2str(u):
    """Convert a UTF-8 Unicode object to a string."""
    return u.encode('utf-8')
