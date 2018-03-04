FROM python:2.7.14-stretch

WORKDIR /root

# Install pipenv and dependencies from Pipfile
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install

# Install additional dependency for Theano
RUN apt-get -qq update && apt-get install -y \
    python-dev

# Include application files and model
COPY *.py ./
COPY skipthoughts/__init__.py skipthoughts/skipthoughts.py skipthoughts/
COPY skipthoughts/models/* skipthoughts/models/

CMD ["pipenv", "run", "./main.py"]
