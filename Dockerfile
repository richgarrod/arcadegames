FROM centos:7

CMD yum install centos-release-scl rh-python36
CMD scl enable rh-python36 bash
CMD pip3 install arcade

WORKDIR /src


