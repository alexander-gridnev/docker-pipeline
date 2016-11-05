import unittest
from pipeline_format import *


class TestFormat(unittest.TestCase):
    def test_format(self):
        example = [
            'some',
            'test',
            'encode'
        ]

        line = encode_line(
            example
        )

        decoded = decode_line(
            line
        )

        self.assertEqual(decoded, example)

        decoded = decode_line_prefix(
            line, 1
        )

        self.assertEqual(decoded[0], example[0])
        self.assertEqual(len(decoded), 3)

        parts = line.rstrip('\n').split(';')

        self.assertEqual(len(parts), 3)
        self.assertEqual(parts[1], decoded[1])
        self.assertEqual(parts[2], decoded[2])

        encoded = encode_line_prefix(decoded, 1)

        self.assertEqual(encoded, line)
