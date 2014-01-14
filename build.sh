#!/bin/bash -vex

printf "build docker\n"

rm -rf docker
git clone git@github.com:dotcloud/docker.git
cd docker
git checkout v0.7.5
git archive v0.7.5 --prefix='docker/' --format=tar | gzip -9 > ../lxc-docker-0.7.5.tar.gz
cd ..
rm -rf docker
rpmbuild -bs --nodeps --define "_sourcedir ." --define "_srcrpmdir ." docker.spec
