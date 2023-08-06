# Shopcloud-Streams-CLI

Shopcloud Streams CLI Package thats send the events per PubSub to the 
streams backend where the magic happend.

## Usage

```py
from shopcloud_streams import Event as StreamEvent
Event("de.talk-point.streams/test_fired", {'pk' :'<pk>'}).fire()
```

## Deploy to PyPi

```sh
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/*
```
