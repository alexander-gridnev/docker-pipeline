import logging
from copy import deepcopy

from collections import defaultdict
from tornado.gen import coroutine, sleep

from consul import tornado as consul_tornado

logging.basicConfig()
log = logging.getLogger(__name__)


class CallbackStorage(object):
    def __init__(self):
        self.__storage = []

    def register(self, c):
        if not hasattr(c, '__call__'):
            raise ValueError()

        self.__storage.append(c)

    def deregister(self, c):
        self.__storage.remove(c)

    def call_all(self, *args, **kwargs):
        for c in self.__storage:
            c(*args, **kwargs)


class ServiceWatch(object):
    def __init__(self, watch_interval=10, **consul_kwargs):
        self.__services = defaultdict(list)
        self.__services_by_id = {}
        self.__watch_interval = watch_interval
        self.__consul_kwargs = consul_kwargs

        self.__remove_callbacks = CallbackStorage()
        self.__add_callbacks = CallbackStorage()

    @property
    def remove_callbacks(self):
        return self.__remove_callbacks

    @property
    def add_callbacks(self):
        return self.__add_callbacks

    @property
    def services(self):
        return self.__services

    @property
    def services_by_id(self):
        return self.__services_by_id

    def update_services(self, services):
        # remove services from cache
        for k, v in deepcopy(self.__services_by_id).iteritems():
            if k not in services:
                self.__services_by_id.pop(k)
                self.__services[v['Service']].remove(v)
                self.__remove_callbacks.call_all(k, v)

        # add services to cache
        for k, v in services.iteritems():
            if k not in self.__services_by_id:
                self.__services_by_id[k] = v
                self.__services[v['Service']].append(v)
                self.__add_callbacks.call_all(k, v)

    @coroutine
    def __watch(self, consul):
        while True:
            self.update_services((yield consul.agent.services()))
            yield sleep(self.__watch_interval)

    @coroutine
    def watch(self):
        c = consul_tornado.Consul(**self.__consul_kwargs)
        self.update_services((yield c.agent.services()))

        # spawn watch coroutine
        self.__watch(c)
