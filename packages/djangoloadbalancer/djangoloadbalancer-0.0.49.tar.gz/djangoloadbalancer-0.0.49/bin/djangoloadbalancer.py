import pickle
from multiprocessing.connection import Listener

import django.db.utils
from django_load_balancer.load_balancer_factory import LoadBalancerFactory
from django_load_balancer.local_settings import LOAD_BALANCER

if __name__ == "__main__":
    load_balancer = LoadBalancerFactory.create_load_balancer()
    address = (LOAD_BALANCER['ADDRESS']['HOST'], LOAD_BALANCER['ADDRESS']['PORT'])
    listener = Listener(address, authkey=bytes(LOAD_BALANCER['ADDRESS']['AUTHKEY'], 'utf-8'))

    while True:
        connection = listener.accept()
        while True:
            payload = connection.recv()
            if payload == 'close':
                connection.close()
                break
            else:
                query = pickle.loads(payload)
                while True:
                    result = load_balancer.run_query(query)
                    try:
                        connection.send(pickle.dumps(result))
                        break
                    except django.db.utils.OperationalError:
                        pass
