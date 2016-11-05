# Docker-pipeline

Tool for pipelining processing of data. Built on top of docker infractructure, each worker is a docker container. Inside of a container it uses linux pipes for transfering data between network layer and your worker. The project is in very intial state now, but has working samples.

### 1. Write processing scripts

Now **docker-pipeline** has an implementation of worker wrapper for python only, but it's easy to write worker wrappers for other languages.

```python
#!/usr/bin/python
from pipelining import run


def job(data):
    # your processing here, for example you can return length of data
    return [data, len(data)]


run(job)
```

### 2. Build base images


```bash
$ ./rebuild_images.sh
```


### 3. Build own workers

Use as base image docker-pipeline-worker or docker-pipeline-source, the only difference - source should generate data, and appropriate header, you can find example in ```pipelining/simple_test_source.py``` 

```
FROM docker-pipeline-worker  # or docker-pipeline-source
ADD {add your executable here}
```

### 4. Describe your topology as docker-compose file

```
version: '2'

services:
  source:
    image: your_source
    restart: always

  processing:
    image: your_worker
    restart: always

  another_processing:
    image: your_another_worker
    restart: always
```

### 5. Run!!

```sh
$ docker-compose -f docker-compose-base.yml -f your-docker-compose.yml up -d

```

### 6. Scale

```sh
$ docker-compose scale processing=3 another_processing=4

```