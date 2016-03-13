import base64
import json


default_encoder = base64.b64encode
default_decoder = base64.b64decode


valid_format_example = [{'test': 'data'}, 'data']
encode_format = [
    # routing
    lambda d: default_encoder(json.dumps(d)),
    # data
    default_encoder
]


decode_format = [
    # routing
    lambda d: json.loads(default_decoder(d)),
    # data
    default_decoder
]


delimiter = ';'


def format_assert(format_config, line_parts):
    if len(format_config) != len(line_parts):
        raise ValueError(
            'format does not compatible with this \
            line: "%s", decode format: %s' % (line_parts, format_config)
        )


def decode_line(line, **kwargs):
    return decode_line_prefix(line, **kwargs)


def encode_line(line_parts, **kwargs):
    return encode_line_prefix(line_parts, **kwargs)


def process(seq, processors):
    '''
        process items of seq, with funcions from processors,
        length of seq and processors should be equal
    '''

    return prefix_process(len(seq), seq, processors)


def prefix_process(prefix_size, seq, processors):
    '''
        process prefix_size items of seq, with funcions from processors
    '''
    if len(seq) != len(processors):
        raise ValueError(
                'process can not perform operation, because of different \
                length of sequence and processors \
                seq: %s; processors: %s' % (seq, processors)
            )

    return [
        process(item) if idx < prefix_size else item
        for idx, item, process in zip(
            xrange(prefix_size), seq, processors
        )
    ]


def decode_line_prefix(line, prefix_size=-1,
                       delimiter=delimiter, decode_format=decode_format):
    line_parts = line.split(delimiter, prefix_size)
    return prefix_process(
        prefix_size if prefix_size != -1 else len(line_parts),
        line_parts, decode_format
    )


def encode_line_prefix(line_parts, suffix=None, delimiter=delimiter,
                       encode_format=encode_format):
    '''
        line_parts - can be iterable or not, suffix - bytes
    '''
    effective_parts = line_parts

    if not hasattr(line_parts, '__iter__'):
        effective_parts = [line_parts]

    if suffix is None and len(line_parts) != len(encode_format):
        raise ValueError(
                'if suffix is None, length of line_parts and \
                encode_format should be equal\
                line_parts: %s; encode_format: %s' % (
                    line_parts,
                    encode_format
                )
            )

    encoded = process(effective_parts, encode_format[:len(effective_parts)])
    if suffix:
        encoded += [suffix]

    return delimiter.join(encoded)
