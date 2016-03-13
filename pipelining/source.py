import sys
import time

from pipeline_format import encode_line

routing = {
    'current': 0,
    'routing': [
        'worker',
        'end'
    ]
}


while True:
    sys.stdout.write(encode_line([routing, 'data']))
    time.sleep(1)
