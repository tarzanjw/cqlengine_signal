import cqlengine.connection
import logging.config
from cqlengine.management import sync_table, delete_keyspace
from cqlengine_signal.tests import ModelA, ModelB, ModelA1, ModelA2

_LOG_CONFIG = {

}

_TEST_KEYSPACE = 'test_cqlengine_signal'
_TEST_HOST = ['localhost', ]

def pytest_sessionstart():
    if _LOG_CONFIG:
        logging.config.dictConfig(_LOG_CONFIG)
    cqlengine.connection.setup(_TEST_HOST, _TEST_KEYSPACE)
    sync_table(ModelA)
    sync_table(ModelA1)
    sync_table(ModelA2)
    sync_table(ModelB)


def pytest_sessionfinish():
    # delete_keyspace(_TEST_KEYSPACE)
    pass