import unittest
from pipeline_format import *


class TestFormat(unittest.TestCase):
    def test_default_format(self):
        self.assertEqual(len(encode_format), len(decode_format))

        line = encode_line(valid_format_example)
        decoded = decode_line(line)

        self.assertEqual(decoded, valid_format_example)

        with self.assertRaises(ValueError):
            encode_line([])

        with self.assertRaises(ValueError):
            decode_line('')

    def test_format(self):
        example = [
            'some',
            'test',
            'encode'
        ]

        decode_format = [
            default_decoder,
            default_decoder,
            default_decoder
        ]

        encode_format = [
            default_encoder,
            default_encoder,
            default_encoder
        ]

        line = encode_line(
            example, encode_format=encode_format
        )

        decoded = decode_line(
            line, decode_format=decode_format
        )

        self.assertEqual(decoded, example)

        decoded = decode_line_prefix(
            line, 1, decode_format=decode_format
        )

        self.assertEqual(decoded[0], example[0])
        self.assertEqual(len(decoded), 2)

    def test_process(self):
        self.assertEqual(process([1, 2], [
                lambda x: x + x,
                lambda x: x * x
            ]),
            [2, 4]
        )

        self.assertEqual(prefix_process(2, [1, 2, 3], [
                lambda x: x + x,
                lambda x: x * x,
                lambda x: x + 1
            ]),
            [2, 4]
        )

        with self.assertRaises(ValueError):
            process([1, 2, 3], [
                lambda x: x + x,
                lambda x: x * x
            ])

        with self.assertRaises(ValueError):
            process([1], [
                lambda x: x + x,
                lambda x: x * x
            ])
