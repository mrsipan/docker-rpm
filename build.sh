#!/bin/bash -vex

VERSION="0.7.5"
printf "build docker\n"

rm -rf docker
git clone git@github.com:dotcloud/docker.git
cd docker
git checkout v${VERSION}
git archive v${VERSION} --prefix="docker-${VERSION}/" --format=tar | gzip -9 > ../lxc-docker-${VERSION}.tar.gz
cd ..
rm -rf docker
rpmbuild -bs --nodeps --define "_sourcedir ." --define "_srcrpmdir ." docker.spec
