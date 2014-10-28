__all__ = ['CassandraPlugin',]

import inspect

from bottle import PluginError, response

import cassandra
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


class CassandraPlugin(object):
    """
    Cassandra Plugin for Bottle.
    Instantiates the Datastax CQL3/Native driver for the environment
    """

    def get_cassandra(self):
        """Return the cassandra connection from the environment."""
        return self.connection

    def __init__(self, endpoints=['127.0.0.1'], 
            keyspace=None, 
            consistency_level=cassandra.ConsistencyLevel.QUORUM,
            keyword='cqlconnection', 
            port=9042,
            compression=True,
            auth_provider=None,
            load_balancing_policy=None,
            reconnection_policy=None,
            default_retry_policy=None,
            conviction_policy_factory=None,
            metrics_enabled=False,
            connection_class=None,
            ssl_options=None,
            sockopts=None,
            cql_version=None,
            protocol_version=2,
            executor_threads=2,
            max_schema_agreement_wait=10,
            control_connection_timeout=2.0,
            **kwargs):
        self.cluster =  Cluster(endpoints, 
                                port=port, 
                                compression=compression,
                                auth_provider=auth_provider,
                                load_balancing_policy=load_balancing_policy,
                                reconnection_policy=reconnection_policy,
                                default_retry_policy=default_retry_policy,
                                conviction_policy_factory=conviction_policy_factory,
                                metrics_enabled=metrics_enabled,
                                connection_class=connection_class,
                                ssl_options=ssl_options,
                                sockopts=sockopts,
                                cql_version=cql_version,
                                protocol_version=protocol_version,
                                executor_threads=executor_threads,
                                max_schema_agreement_wait=max_schema_agreement_wait,
                                control_connection_timeout=control_connection_timeout
                                )
        self.keyspace = keyspace
        self.connection = self.cluster.connect(self.keyspace)
        self.consistency_level = consistency_level
        self.name = "cqlconnection"
        self.keyword = keyword

    def __str__(self):
        return "bottle_cassandra_plugin.CassandraPlugin(keyword=%r)" % (self.keyword)

    def __repr__(self):
        return "bottle_cassandra_plugin.CassandraPlugin(keyword=%r)" % (self.keyword)

    def setup(self, app):
        """Called as soon as the plugin is installed to an application."""
        for other in app.plugins:
            if not isinstance(other, CassandraPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another Cassandra plugin with "
                                  "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        """Return a decorated route callback."""
        args = inspect.getargspec(context['callback'])[0]
        # Skip this callback if we don't need to do anything
        if self.keyword not in args:
            return callback

        def wrapper(*a, **ka):
            ka[self.keyword] = self.get_cassandra()
            rv = callback(*a, **ka)
            return rv

        return wrapper

    def execute(self, cql_query, cql_query_params={}, consistency_level=None, timeout=10.0):
        if consistency_level is None:
            cl = consistency_level
        else:
            cl = self.consistency_level

        prep_query = SimpleStatement(cql_query, cl)
        return self.connection.execute(prep_query, parameters=cql_query_params, timeout=timeout)

