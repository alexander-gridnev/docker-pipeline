#!/usr/bin/python -u
from pipelining import run


def job(data):
    return [data, len(data)]


run(job)
