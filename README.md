bottle-cassandra-driver
=======================

Trivial Cassandra Driver plugin for the Bottle web framework

Install
=======================

Using pip:
```
pip install bottle_cassandra_driver
```

Using easy_install:
```
easy_install bottle_cassandra_driver
```

From Github:

Download:
```
git clone https://github.com/jeffjirsa/bottle-cassandra-driver.git
```

Then, Build & Install:
```
cd bottle-cassandra-driver && python setup.py build && sudo python setup.py install
```

Use
=======================

```

import json
import bottle
import bottle_cassandra_driver


from bottle import request, response, get, post, put, delete

app = application = bottle.Bottle()
application = bottle.default_app()

bottle_host='127.0.0.1'
bottle_port=80

cql_plugin = bottle_cassandra_driver.CassandraPlugin(endpoints=['127.0.0.1'], keyspace='example')
bottle.install(cql_plugin)


@get(['/'])
def route_index(cqlconnection):
    rows = cqlconnection.execute("SELECT account_id FROM accounts")
    output = []
    for r in rows:
        output.append(str(r.account_id))
    return bottle.HTTPResponse(status=200, body=json.dumps(output))

bottle.run(host=bottle_host, port=bottle_port, reloader=bottle.DEBUG)

```
