import random
import logging
import socket

from pipeline_format import encode_line_prefix, decode_line_prefix
from async_pipelining import AsyncStream

from discovering.consul_watcher import ServiceWatch
from tornado.tcpclient import TCPClient
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.gen import coroutine

import sys


logging.basicConfig()
log = logging.getLogger(__name__)


class ClientApp(object):
    def __init__(self):
        self.__services = ServiceWatch(host='consul')

        self.__services.add_callbacks.register(self.service_added)
        self.__services.remove_callbacks.register(self.service_removed)

        self.__clients = {}
        self.__reconnection = list()

    def service_removed(self, service_id, data):
        if data in self.__reconnection:
            self.__reconnection.remove(data)
        self.__clients.pop(service_id, None)

    def service_added(self, service_id, data):
        self.__reconnection.append(data)

    @coroutine
    def refresh_connections(self, service):
        streams_futures = [
            (
                TCPClient().connect(
                    socket.gethostbyname(source['ID'].split(':')[1]),
                    source['Port']
                ),
                source
            )
            for source in self.__reconnection if source['Service'] == service
        ]

        for stream_future, source in streams_futures:
            try:
                self.__clients[source['ID']] = yield stream_future
                self.__reconnection.remove(source)
            except Exception as e:
                log.exception(e)
                log.warning('will reconnect %s' % source)

    @coroutine
    def work_cycle(self):
        stream = AsyncStream(0)

        yield self.__services.watch()

        while True:
            try:
                line = yield stream.read_line()
            except StreamClosedError:
                break

            parts = decode_line_prefix(line, 1)
            route = parts[0]

            next_service = route['routing'][route['current']]
            route['current'] += 1

            new_data = encode_line_prefix(parts, 1)

            yield self.refresh_connections(next_service)

            service = random.choice(self.__services.services[next_service])

            print(next_service, service)

            try:
                client = self.__clients[service['ID']]
                sys.stderr.write(new_data)
                yield client.write(new_data)
            except Exception as e:
                log.exception(e)
                self.__clients.pop(service['ID'], None)
                self.__reconnection.append(service)


def run():
    app = ClientApp()

    @coroutine
    def wrap():
        yield app.work_cycle()

    IOLoop.current().run_sync(wrap)
