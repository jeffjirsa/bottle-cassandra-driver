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



