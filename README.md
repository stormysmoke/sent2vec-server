# Sent2Vec

This is the Sent2Vec back-end. It allows to index the sentences of a text (encoding them as vectors), and then to retrieve the "nearest neighbours" of a query sentence.

## Conceptual Usage Example

~~~
index("This is a sentence. Another sentence. And so on...")
query("That's the query sentence.", 3)
~~~

The seond argument of the `query` method is the number of nearest neighbours to return.

The `query` method returns the specified number of nearest neighbour sentences along with their "distances" to the query sentence. The smaller the distances, the more similar are the two sentences in meaning.

## Deployment

### Compute Instance Requirements

- RAM: the full machine learning model is around 5.5 GB in size. Thus, the compute instance must provide at least this amount of RAM (and hard disk storage).
- CPUs: I observed no significant performance difference when the app runs on 1, 2, or 4 CPUs. 

In general, a [t2.large](https://aws.amazon.com/ec2/instance-types/t2/) EC2 instance on AWS seems to work fine.

### Docker Image

The application is provided as the Docker image [stormysmoke/sent2vec-back](https://hub.docker.com/r/stormysmoke/sent2vec-back/) on Docker Hub.

The machine learning model is included in the Docker image, so the image is quit large. The image versions with a `x.x.x-dev` tag contain a pruned version of the model, which is smaller and loads faster, but doesn't produce any meaningful results. This one is only for development. The image versions with a `x.x.x` version tag contain the full model and are supposed to be used in production.

### Deployment Steps

#### 1. Start up a RabbitMQ server and note its URI

The application connects to a RabbitMQ server on startup based on the URI that you provide. A RabbitMQ URI has the following form:

~~~
amqp://user:password@host:port/
~~~

#### 2. Install Docker

On Ubuntu:

~~~bash
sudo apt-get update
sudo apt-get -y install docker.io
~~~

#### 3. Download and run the Docker image

~~~bash
docker run -d -e RABBITMQ_URI=<uri> stormysmoke/sent2vec-back:<tag>
~~~

Replace `<uri>` with the URI of the running RabbitMQ server that you noted in step 1, and replace `<tag>` with the tag corresponding to the desired version of the image to run.

You can inspect the output of the application with `docker logs <container>`, where `<container>` is the container ID of the container that you just started.

That's it! That's how easy it is to deploy an application with Docker!

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
{"result": [["Sentence 1", "Sentence 2", "Sentence 3"], [0.84, 0.94, 1.04]]}
~~~
