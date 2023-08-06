# Cobnut
[![Test](https://github.com/JeremyAndress/cobnut/actions/workflows/python-app.yml/badge.svg)](https://github.com/JeremyAndress/cobnut/actions/workflows/python-app.yml) [![license](https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg)](LICENSE)

Simple cache management to make your life easy.

### Requirements 
- Python 3.6+ 

### Installation
```sh
pip install cobnut
```

### Quick Start
For the tutorial, you must install redis as dependency

```sh
pip install cobnut[redis]
```


The simplest Cobnut setup looks like this:

```python
from cobnut import Cobnut, RedisModel

cobnut = Cobnut(redis_connection=RedisModel(host="localhost"))
cobnut.set(key='mykey', data='mydata')
cobnut.get(key='mykey')
# Response: mydata

cobnut.delete(key='mykey')
cobnut.get(key='mykey')
# Response: None

```