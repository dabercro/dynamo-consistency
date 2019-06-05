FROM sl:7
MAINTAINER Daniel Abercrombie <dabercro@mit.edu>

# Users for Dynamo installation
RUN useradd mysql && useradd dynamo -u 500

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

RUN yum -y install \
    initscripts \
    lighttpd \
    lighttpd-fastcgi \
    mariadb \
    mariadb-server \
    fetch-crl \
    python-flup \
    python-fts \
    rrdtool-python \
    condor-python \
    python-pip \
    python-devel \
    gcc \
    mariadb-devel \
    libyaml-devel \
    git \
    perl

RUN pip install -U MySQL-python 'matplotlib<3' requests 'pip==18.0'
RUN pip install 'cx_Oracle'

# Get the Dynamo source. Fixed to a specific commit now.
RUN printf 'git clone https://github.com/SmartDataProjects/dynamo.git\ncd dynamo\ngit checkout 330c00334bfd42dc82e5ca975a8568a7731c1979' | bash
RUN printf 'cd dynamo\ncp defaults.json.template defaults.json\ncp dynamo.cfg.template dynamo.cfg\ncp mysql/grants.json.template mysql/grants.json' | bash

# Install MariaDB
# Will need to run 'mysqld_safe &' at startup for tests
RUN sed -i 's/require rpm/#/g' /dynamo/install.sh
RUN sed -i 's/require rpm/#/g' /dynamo/mysql/install.sh

RUN printf "mysql_install_db --user=mysql\nmysqld_safe &\nsleep 5\nmysqladmin -u root password 'test'\ncd /dynamo\nprintf 'test\\n' | ./install.sh\necho \"GRANT ALL ON dynamo.* TO 'dynamo'@'localhost'; GRANT ALL ON dynamoregister.* TO 'dynamo'@'localhost';\" | mysql -ptest\nkill %%1\n" | bash

# Install pdflatex
RUN yum install -y wget
RUN curl -L http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz > install-tl-unx.tar.gz && tar -xf install-tl-unx.tar.gz
RUN cd install-tl-2* && printf 'S\nd\nR\nI\n' | ./install-tl
RUN cd /usr/local/texlive/2*/bin/*/ && ./tlmgr install xcolor pgf pgfplots standalone xkeyval

RUN echo "export PATH=`echo /usr/local/texlive/2*/bin/*/`:$PATH" >> ~/.bashrc
