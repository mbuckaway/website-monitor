FROM python:3.9-buster

RUN echo "America/Toronto" > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/America/Toronto /etc/localtime && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --no-install-suggests -y \
    apt-transport-https \
    ca-certificates \
    vim \
    less
   
COPY webmonlib setup.py /src

RUN rm -rf /var/lib/apt/lists/* && \
    cd /src && \
    python3 setup.py install

# Add more code here to get the container started correctly

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
