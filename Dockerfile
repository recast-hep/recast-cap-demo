FROM cern/cc7-base
RUN yum install -y gcc gcc-c++ graphviz-devel ImageMagick python-devel libffi-devel openssl openssl-devel unzip nano autoconf automake libtool openssh-clients
RUN curl https://bootstrap.pypa.io/get-pip.py | python -
COPY . /recast_yadage_plugin
WORKDIR /recast_yadage_plugin
RUN pip install https://github.com/recast-hep/recast-celery/archive/master.zip --process-dependency-links
RUN pip install https://github.com/diana-hep/packtivity/archive/master.zip --process-dependency-links
RUN pip install https://github.com/diana-hep/yadage/archive/master.zip --process-dependency-links
RUN pip install -e . --process-dependency-links
RUN echo bust6
RUN pip install https://github.com/lukasheinrich/packtivity-reana-backend/archive/master.zip
ENV PACKTIVITY_ASYNCBACKEND packtivity_reana_backend.backend:ExternalBackend:ExternalProxy
