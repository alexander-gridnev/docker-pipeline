#!/usr/bin/python -u

from async_pipelining import run
from tornado.gen import coroutine


@coroutine
def job(args):
    args[1] = str(len(args[1]))


run(job)
