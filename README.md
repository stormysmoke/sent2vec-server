# QuantumSense - Sent2Vec

This is the Sent2Vec application. It allows to index the sentences of a text (encoding them as vectors), and then to retrieve the "nearest neighbours" of a query sentence.

## Conceptual Usage Example

~~~
index("This is a sentence. Another sentence. And so on...")
query("That's the query sentence.", 3)
~~~

The seond argument of the `query` method is the number of nearest neighbours to return.

The `query` method returns the specified number of nearest neighbour sentences along with their "distances" to the query sentence. The smaller the distances, the more similar are the two sentences in meaning.

## Deployment

The application is designed to be deployed to a IaaS platform like Google Cloud Platform (GCP) Compute Engine or Amazon Web Services (AWS) EC2. I tested it only on GCP Compute Engine.

### Compute Instance Requirements

The used machine learning model is around 5.5 GB in size. Thus, the compute instance must provide at least this amount of memory and hard disk space.

For a decent peformance, the compute instance should have at least 2 CPUs. I have tested the app on a GCP Compute Engine instance with a single CPU, and the performance is quite bad (indexing a 2500 word text takes more than 1 minute vs. 30 seconds on my MacBook Air).

### Deployment Instructions

The following applies to deployment on **GCP Compute Engine** with a **Debian 8.0** image.

First of all, you have to copy all the files of this application, including the 5.5 GB model files, to your GCP Compute Engine instance. You can do this for example by cloning this repository to your instance (just first install Git with `sudo apt-get install git-core`). The model files you can download from the URLs listed in the `URL.txt` file in the `models/` directory, for example with `wget -i URL.txt`. You could also upload them from your local machine with `scp`, if you have them locally.

When all the files are deployed, you have to do the following (all from within the application root directory):

Install the Python dependencies and create Python virtual environment:

~~~bash
pipenv install
~~~

Install special dependencies for Theano:

~~~bash
sudo apt-get install python-dev
~~~

That's it! Then you can launch the application with:

~~~bash
pipenv run ./main.py
~~~

You have to use Pipenv to run the script, because the Python dependencies have been installed only to this specific virtual environment, and Pipenv runs the provided command within this virual environment.


## Communication

The application connects to a RabbitMQ server (running on Heroku) and acts as a RPC server. The message format is inspired by JSON-RPC 2.0 (and eventually should be conformant with this standard), and currently looks as follows:

### Method: `index`

Request:

~~~json
{"method": "index", "params": "This is a sentence. And so on..."}
~~~

Response:

~~~json
{"result": null}
~~~

### Method: `query`

Request:

~~~json
{"method": "query", "params": ["That's the query sentence.", 3]}
~~~

Response:

~~~json
{"result": [["Sent 1", "Sent 2", "Sent 3"], [0.84, 0.94, 1.04]]
~~~
