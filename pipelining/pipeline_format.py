import msgpack


delimiter = ';'


def decode_line(line):
    return map(msgpack.unpackb, line.rstrip('\n').split(delimiter))


def encode_line(line_parts):
    return delimiter.join(map(msgpack.packb, line_parts)) + '\n'


def decode_line_prefix(line, prefix_size):
    line_parts = line.rstrip('\n').split(delimiter)
    return (map(msgpack.unpackb, line_parts[:prefix_size]) +
            line_parts[prefix_size:])


def encode_line_prefix(line_parts, prefix_size):
    '''
        line_parts - can be iterable or not, suffix - bytes
    '''

    return delimiter.join(
        map(
            msgpack.packb,
            line_parts[:prefix_size]
        ) + line_parts[prefix_size:]
    ) + '\n'
