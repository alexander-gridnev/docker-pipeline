#!/usr/bin/python -u
from pipelining import run


def job(args):
    args[1] = len(args[1])


run(job)
