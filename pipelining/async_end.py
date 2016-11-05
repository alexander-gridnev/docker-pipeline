#!/usr/bin/python -u

from async_pipelining import run
from tornado.gen import coroutine, Return

import sys


@coroutine
def job(data, data_len):
    sys.stderr.write('data: %s %s\n' % (data, data_len))
    raise Return([data, data_len])


run(job)
