import abc
import inspect
import pickle
from datetime import datetime

import django.db
import django.db.models

from .query import QueryType


class Executor(abc.ABC):
    @abc.abstractmethod
    def run_query(self, query, database):
        pass


class QueryExecutor(Executor):
    def run_query(self, query, database):
        if query.method == 'get_queryset':
            instance = query.model.loadbalancer_base_manager
            result = instance.__getattribute__(query.method)(*query.args, **query.kwargs).using(database.name)
        elif query.type == QueryType.NO_QUERYSET.value:
            instance = query.model
            result = dict(inspect.getmembers(django.db.models.Model))[query.method](instance, using=database.name)
        else:
            instance = query.model.models_manager.using(database.name)
            result = instance.__getattribute__(query.method)(*query.args, **query.kwargs)
        result = pickle.dumps(result)
        database.load_balancer.end_query(query, result)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{current_time}   {database.name}   {query.model}   {query.method}")


class InfoQueryExecutor(Executor):
    def run_query(self, query, database):
        with django.db.connections[database.name].cursor() as cursor:
            new_info = self.get_statistic(query, cursor, database)
            database.info.put(new_info)

    def get_statistic(self, query, cursor, database):
        pass
