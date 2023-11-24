# MongoUtils
Some utils to deal with MongoDB more easily.

## Connect to database
Simple function to connect to MongoDB or a specific database. 

### Connect to MongoDB server

```python
from monutils import connect
from monutils import Mode

# Connect to localhost in the default port without authentication
client = connect()
# Connect to a host given
client = connect(host, port)
# Using replicaset
client = connect(host, port, replicaset)
# Connect to MongoDB using user and password
client = connect(host, port, replicaset, user, password)
# Without replicaset
client = connect(host, port, None, user, password)
client = connect(host, port, user=user, password=password)
# Select the authentication mechanism (if mode is not set, then it tries all possible authentication methods)
client = connect(host, port, replicaset, user, password, mode=Mode.SCRAM_SHA_256)
# Using certificates
client = connect(host, port, replicaset, user, password, cert_key_file, ca_file, mode=Mode.SCRAM_SHA_256)
# Using session token
client = connect(host, port, replicaset, user, password, session_token=token, mode=Mode.SCRAM_SHA_256)
```

### Connect to MongoDB database

```python
from monutils import connect_database
from monutils import Mode

# Connect to localhost in the default port without authentication
client = connect_database(databasse=database)
# Connect to a host given
client = connect_database(host, port, database=database)
# Using replicaset
client = connect_database(host, port, replicaset, database)
# Connect to MongoDB using user and password
client = connect_database(host, port, replicaset,
                          database, user, password)
# Without replicaset
client = connect_database(host, port, None, database, user, password)
client = connect_database(host, port, 
                          database=database, user=user, password=password)
# Select the authentication mechanism 
# (if mode is not set, then it tries all possible authentication methods)
client = connect_database(host, port, replicaset, database, user, 
                          password, mode=Mode.SCRAM_SHA_256)
# Using certificates
client = connect_database(host, port, replicaset, database, user, password, 
                          cert_key_file, ca_file, mode=Mode.SCRAM_SHA_256)
# Using session token
client = connect_database(host, port, replicaset, database, user, password, 
                          session_token=token, mode=Mode.SCRAM_SHA_256)
```

## Copy collections
You can copy collection from a database to another easily.

```python
from monutils import copy

from_client = connect(...) # Connection with the source MongoDB server
to_client = connect(...) # Connection with the target MongoDB server
# Copy the collection
copy(from_client, to_client, from_db, to_db, from_collection, to_collection)
# Copy de collection ignoring copy errors
copy(from_client, to_client, from_db, to_db, from_collection, to_collection, True)
```

## Create a cache mongodb database

```python
from monutils import connect
from monutils.cache import MongoCache

client = connect(...)
db = client['my_db']
# Create a cache without storage limit
cache = MongoCache(db['my_collection'])
# Add an element to the collection
cache[key] = value
cache.add(key, value)
# Update an existing element to the collection
cache.update(key, value)
# Remove an element from the collection
cache.remove(key)
# Retrieve an element from the collection
cache[key]
# Check if the element is in the collection
key in cache
# Calculate the cache size
cache.size
# Create a cache limited to 1000 elements
cache = MongoCache(db['my_collection'], 1000)
```