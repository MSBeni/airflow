from airflow.hooks.base import BaseHook
from elasticsearch import Elasticsearch

class ElasticHook(BaseHook):
    def __init__(self, conn_id='elasticsearch_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(conn_id)

        conn_config = {}
        hosts = []

        if conn.host:
            hosts = conn.host.split(',')

        if conn.port:
            conn_config['port'] = int(conn.port)

        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)


