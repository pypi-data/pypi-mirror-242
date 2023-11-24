import unittest

from mysutils.yaml import load_yaml

from monutils import connect, Mode


class MyTestCase(unittest.TestCase):
    def test_something(self):
        config = load_yaml('credentials.yml')
        host, port, user, password = config['host'], config['port'], config['user'], config['password']
        with connect(host=host, port=port, user=user, password=password, replicaset='rs0', mode=Mode.AUTO) as client:
            print(client.server_info())
            print(client.list_database_names())



if __name__ == '__main__':
    unittest.main()
