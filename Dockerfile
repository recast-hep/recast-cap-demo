FROM cern/cc7-base
COPY . /code
WORKDIR /code
RUN curl -fsSL https://get.docker.com/ | sh
RUN yum install -y gcc graphviz-devel imagemagick python-devel
RUN curl https://bootstrap.pypa.io/get-pip.py | python -
RUN pip install -e .
