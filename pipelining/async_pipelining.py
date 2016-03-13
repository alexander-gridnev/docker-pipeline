from tornado.ioloop import IOLoop
from tornado.iostream import PipeIOStream, StreamClosedError
from tornado.gen import coroutine

from pipeline_format import encode_line, decode_line


class AsyncStream(PipeIOStream):
    def read_line(self):
        return self.read_until('\n')


@coroutine
def work_cycle(job):
    stream = AsyncStream(0)
    out = AsyncStream(1)

    while True:
        try:
            line = yield stream.read_line()
        except StreamClosedError:
            break

        parts = decode_line(line)
        yield job(parts)
        yield out.write(encode_line(parts))


def run(job):
    @coroutine
    def wrap():
        yield work_cycle(job)

    IOLoop.current().run_sync(wrap)
