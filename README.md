# Sent2Vec Server

The Sent2Vec server application. It allows to encode a text as sentence vectors, and then extract the nearest neighbour sentences of a query sentence.

## Conceptual Usage Example

~~~
index("This is a sentence. Another sentence. And so on...")
query("That's the query sentence.", 3)
~~~

The second argument of the `query` method is the number of nearest neighbours to return.

The `query` method returns the specified number of nearest neighbour sentences along with their "distances" to the query sentence. The smaller the distances, the more semantically similar are the sentences.

## Docker Image

[stormysmoke/sent2vec-server](https://hub.docker.com/r/stormysmoke/sent2vec-server/)

The versions with a `*-dev` tag contain a stripped-down model that does not return meaningful result, but is faster to load. It is to be used during development only.

## Compute Instance Requirements

The Docker image is currently about 7 GB in size (most of this space is due to the Sent2Vec model). Thus, a computing instance to run the image has the following minimum requirements:

- 14 GB free disk storage (double the size of the image for extracting the image after downloading it)
- 7 GB RAM
- 1 CPU (performance with more CPUs might be better, but I didn't test it)

In general, it works fine on a [t2.large](https://aws.amazon.com/ec2/instance-types/t2/) EC2 instance on AWS.

## Dependencies

The Sent2Vec server uses several other services which must be set up before starting this application.

### RabbitMQ

Make sure you have a running RabbitMQ server listening on the default port 5672.

For development, I often use a RabbitMQ server additionally listening on port 1723, because in some network outgoing connections to port 5672 are blocked by the firewall.

You will need the URI of this server.

A RabbitMQ server URI has the following format:

~~~
amqp://user:password@host:port/virtualhost
~~~

### AWS S3

Create an S3 bucket and note the following information about it:

- Name of the bucket
- AWS access key of an AWS account that has write access to this bucket
- AWS secret access key of this AWS account


## Run

### Direct

You can run the Docker image directly with:

~~~bash
docker run \
    -d \
    -e RABBITMQ_URI=<uri> \
    -e S3_BUCKET_NAME=<bucket> \
    -e AWS_ACCESS_KEY_ID=<key> \
    -e AWS_SECRET_ACCESS_KEY=<secret-key> \
    stormysmoke/sent2vec-server:<tag>
~~~

### Script

Alternatively, you can run the image with the [`bin/run`](https://raw.githubusercontent.com/stormysmoke/sent2vec-server/master/bin/run) script as follows:

~~~bash
bin/run <tag>
~~~

Or in a single command including the download of the script:

~~~bash
curl -Lks https://raw.githubusercontent.com/stormysmoke/sent2vec-server/master/bin/run | bash -s <tag>
~~~

Where `<tag>` is the desired version to run.

For this to work, you have to create the file `.env` in the current working directory with the following content:

~~~bash
export RABBITMQ_URI=<uri>
export S3_BUCKET_NAME=<bucket>
export AWS_ACCESS_KEY_ID=<key>
export AWS_SECRET_ACCESS_KEY=<secret-key>
~~~

Set the values of the variables in `.env` to the appropriate information that you took not in the *Dependencies* section.

*Note: by convention, if using a `*-dev` tag of the image, then the file must be called `.env-dev` instead of `.env`.*

## Communication

Client and server exchange plain text messages via RabbitMQ. the message format is inspired by [JSON RPC 2.0](http://www.jsonrpc.org/specification) (and eventually should be identical with it). 

Currently, the request and response messages look as follows:

### Method: `encode`

Request:

~~~json
{"method": "encode", "params": {"text": "Bla bla blah..."}, "id": "1234"}
~~~

Response:

~~~json
{"result": {"id": "abcd"}, "id": "1234"}
~~~

### Method: `knn`

Request:

~~~json
{"method": "knn", "params": {"query": "That's the query sentence.", "k": 3, "id": "abcd"}, "id": "2345"}
~~~

Response:

~~~json
{"result": {"sent": ["Bla bla", "Bla blah", "Bla bla bla"], "dist": [0.84, 0.94, 1.04]}, "id": "2345"}
~~~
