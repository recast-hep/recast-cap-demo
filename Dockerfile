FROM fedora:27
RUN dnf install -y \
      autoconf \
      automake \
      gcc \
      gcc-c++ \
      graphviz-devel \
      hostname \
      ImageMagick \
      libffi-devel \
      less \
      libtool \
      nano \
      openssl \
      openssl-devel \
      openssh-clients \
      python-devel \
      redhat-rpm-config \
      unzip \
      wget \
      which \
      git \
      ;
RUN curl https://bootstrap.pypa.io/get-pip.py | python - && \
    curl -sSL https://get.docker.com/builds/Linux/x86_64/docker-1.9.1  -o /usr/bin/docker && chmod +x /usr/bin/docker && \
    curl -sSL https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 -o /usr/bin/jq && chmod +x /usr/bin/jq

RUN dnf install -y nodejs
RUN npm install -g bower;  echo '{ "allow_root": true }' > /root/.bowerrc

RUN echo bus55t1211

ARG WFLOW_BACKEND_TAG=master
RUN pip install celery


RUN pip install https://github.com/recast-hep/wflow-backend/archive/${WFLOW_BACKEND_TAG}.zip --process-dependency-links

COPY . /yadage_plugin
WORKDIR /yadage_plugin
RUN cd wflowyadageworker/resources/server_static; bower install
RUN pip install -r yadage_requirements.yml
RUN pip install -e . --process-dependency-links
