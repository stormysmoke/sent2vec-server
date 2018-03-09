FROM python:2.7.14-stretch

WORKDIR /root

# Download model files (do this first, to prevent that it needs to be repeated
# when a change in another command invalidates the Docker build cache)
RUN wget -P skipthoughts/models --no-verbose \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/dictionary.txt \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/utable.npy \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/btable.npy \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/uni_skip.npz \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/uni_skip.npz.pkl \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/bi_skip.npz \
    https://stormysmoke.s3.amazonaws.com/skipthoughts/models/dev/bi_skip.npz.pkl

#RUN wget -P skipthoughts/models --no-verbose \
#    http://www.cs.toronto.edu/~rkiros/models/dictionary.txt \
#    http://www.cs.toronto.edu/~rkiros/models/utable.npy \
#    http://www.cs.toronto.edu/~rkiros/models/btable.npy \
#    http://www.cs.toronto.edu/~rkiros/models/uni_skip.npz \
#    http://www.cs.toronto.edu/~rkiros/models/uni_skip.npz.pkl \
#    http://www.cs.toronto.edu/~rkiros/models/bi_skip.npz \
#    http://www.cs.toronto.edu/~rkiros/models/bi_skip.npz.pkl

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependency for Theano
RUN apt-get -qq update && apt-get install -y python-dev && apt-get clean

# Include application files
COPY *.py ./
COPY skipthoughts/__init__.py skipthoughts/skipthoughts.py skipthoughts/

CMD ["python", "-u", "main.py"]
