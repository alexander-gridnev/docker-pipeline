#!/usr/bin/python -u
import sys

from pipeline_format import encode_line, decode_line


def run(job):
    while True:
        parts = decode_line(sys.stdin.readline())
        job(parts)
        sys.stdout.write(encode_line(parts))
