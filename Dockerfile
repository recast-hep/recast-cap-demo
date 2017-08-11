FROM fedora
RUN dnf install -y gcc gcc-c++ graphviz-devel ImageMagick python-devel libffi-devel openssl openssl-devel unzip nano autoconf automake libtool openssh-clients
RUN dnf install -y dnf redhat-rpm-config hostname which wget less
RUN curl https://bootstrap.pypa.io/get-pip.py | python -
COPY . /yadage_plugin
WORKDIR /yadage_plugin
RUN curl -sSL https://get.docker.com/builds/Linux/x86_64/docker-1.9.1  -o /usr/bin/docker && chmod +x /usr/bin/docker
RUN curl -sSL https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -o /usr/bin/jq && chmod +x /usr/bin/jq
RUN pip install celery
RUN pip install https://github.com/recast-hep/wflow-celery/archive/master.zip --process-dependency-links
RUN pip install -r yadage_requirements.yml
RUN pip install -e . --process-dependency-links
