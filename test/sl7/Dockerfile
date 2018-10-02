FROM sl:7
MAINTAINER Daniel Abercrombie <dabercro@mit.edu>

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

RUN yum -y install \
    python-pip \
    python-devel \
    gcc \
    mariadb-devel \
    libyaml-devel \
    perl

RUN pip install -U 'pip==18.0'
