FROM sl:6
MAINTAINER Daniel Abercrombie <dabercro@mit.edu>

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

RUN yum -y install \
    python-pip \
    python-devel \
    gcc \
    mysql-devel \
    libyaml-devel \
    git \
    perl

RUN pip install -U 'pip==9.0.1'
