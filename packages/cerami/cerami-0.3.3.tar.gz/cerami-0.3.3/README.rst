Cerami
======
Cerami is a python library that hopefully provides some sanity to boto3's DynamoDB client. Its intended use is as a library to help define table data through the creation of models and create sane, readable, and reproducable DynamoDB requests.

Please read the `Full Documentation`_

.. _Full Documentation: https://cerami.readthedocs.io/en/latest/ 

Quickstart
==========

Install
-------

.. code-block::

    pip install cerami

I have boto3 and aws credentials set up
---------------------------------------

.. code-block:: python

    # create the db singleton
    import boto3
    from cerami import Cerami

    dynamodb = boto3.client('dynamodb')
    db = Cerami(dynamodb)


.. code-block:: python

    # create classes that inherit from the singleton
    from cerami.datatype import String, Set, Datetime
    from cerami.decorators import primary_key

    @primary_key('name', 'artist')
    class Album(db.Model):
	__tablename__ = "Albums"

	name = String()
	artist = String()
	songs = Set(String())
	released_date = Datetime()

    # Some Query Examples
    Album.scan \
	.filter(Album.released_date.begins_with("1996")) \
	.execute()

    Album.query \
	.key(Album.name == "The Black Album") \
	.execute()

    Album.get \
	.key(Album.name == "Reasonable Doubt") \
	.key(Album.artist == "Jay-Z") \
	.execute()


I have never used boto3 or dynamodb before
------------------------------------------
You can run DynamoDB locally!

You need to install the aws2 cli and have dynamo db running locally. Dynamodb requires java to run locally as well so good luck if you dont have it. Try these steps first and see how it goes.

Download DynamoDB Locally
~~~~~~~~~~~~~~~~~~~~~~~~~
1. `Download DynamoDB Locally`_
2. Unzip/Untar the content
3. Move to somewhere you wont lose it.

.. _Download DynamoDB Locally: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

Download the AWS2 CLI
~~~~~~~~~~~~~~~~~~~~~
1. `Download the AWS2 CLI`_
2. Follow the install instructions

.. _Download the AWS2 CLI`: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

Configure the AWS2 CLI
~~~~~~~~~~~~~~~~~~~~~~
In order to run DynamoDB locally, you need to configure your aws as such:

.. code-block::

    aws2 configure


.. code-block::

    # These are the actual values to use with the local dynamodb instance
    AWS Access Key ID: "fakeMyKeyId"
    AWS Secret Access Key: "fakeSecretAccessKey"
    us-west-1

Starting DynamoDB Locally
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block::

    java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb


Creating a DynamoDB Table
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    import boto3

    dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:8000")

    dynamodb.create_table(
        TableName='Albums',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'artist',
                'KeyType': 'Range', # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'artist',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


Using Cerami
~~~~~~~~~~~~
.. code-block:: python

    # Create the db singleton
    import boto3
    from cerami import Cerami

    dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
    db = Cerami(dynamodb)

.. code-block:: python

    # create classes that inherit from the singleton
    from cerami.datatype import String, Set, Datetime
    from cerami.decorators import primary_key

    @primary_key('name', 'artist')
    class Album(db.Model):
	__tablename__ = "Albums"

	name = String()
	artist = String()
	songs = Set(String())
	released_date = Datetime()

