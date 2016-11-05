import sys
import time

from pipeline_format import encode_line

routing = {
    'current': 0,
    'routing': [
        'docker-pipeline-worker',
        'docker-pipeline-end'
    ]
}


i = 0
while True:
    sys.stdout.write(encode_line([routing, 'data%s' % i]))
    time.sleep(1)
    i += 1
