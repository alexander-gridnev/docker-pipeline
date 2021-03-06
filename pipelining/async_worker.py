#!/usr/bin/python -u

from async_pipelining import run
from tornado.gen import coroutine, Return

import sys


@coroutine
def job(data):
    sys.stderr.write('data: %s\n' % data)
    raise Return([data, len(data)])


run(job)
