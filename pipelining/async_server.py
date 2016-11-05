from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from async_pipelining import AsyncStream
from tornado.gen import coroutine

import sys


class InServer(TCPServer):
    out = AsyncStream(1)

    @coroutine
    def handle_stream(self, stream, *args, **kwargs):
        while True:
            try:
                line = yield stream.read_until(b'\n')
            except StreamClosedError:
                break

            sys.stderr.write(line)
            yield self.out.write(line)


server = InServer()
server.listen(7000)
IOLoop.current().start()
