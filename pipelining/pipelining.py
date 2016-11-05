#!/usr/bin/python -u
import sys

from pipeline_format import encode_line, decode_line


def run(job):
    while True:
        parts = decode_line(sys.stdin.readline())
        new_parts = job(*parts[1:])
        sys.stdout.write(encode_line([parts[0]] + new_parts))
