FROM cern/cc7-base
RUN yum install -y gcc gcc-c++ graphviz-devel ImageMagick python-devel libffi-devel openssl openssl-devel unzip nano autoconf automake libtool openssh-clients
RUN curl https://bootstrap.pypa.io/get-pip.py | python -
COPY . /recast_yadage_plugin
WORKDIR /recast_yadage_plugin
RUN curl https://get.docker.com/builds/Linux/x86_64/docker-1.9.1  -o /usr/bin/docker && chmod +x /usr/bin/docker
RUN echo bustit4
RUN pip install https://github.com/recast-hep/recast-celery/archive/master.zip --process-dependency-links
RUN pip install https://github.com/diana-hep/packtivity/archive/master.zip --process-dependency-links
RUN pip install https://github.com/diana-hep/yadage/archive/master.zip --process-dependency-links
RUN pip install -e . --process-dependency-links
