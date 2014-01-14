# install lxc-docker at /opt/docker

%define debug_package %{nil}
%define __strip /bin/true

Name: lxc-docker
Version: 0.7.5
Release: 2%{?dist}
Summary: docker containers
Group: Development/Languages
License: BSD
URL: http://docker.io
AutoReqProv: no

# use a dummy tar
#Source0: dummy.tar.gz
Source0: lxc-docker-%{version}.tar.gz
Source1: dockerd.service
Source2: docker.sysvinit
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: go
BuildRequires: git
BuildRequires: curl
BuildRequires: mercurial
BuildRequires: sqlite-devel
BuildRequires: device-mapper-devel

Requires: lxc
Requires: curl
Requires: go
Requires: git
Requires: tar

Obsoletes: docker-container

%description
Docker Application Container

%prep
%setup -c lxc-docker-%{version}

%build
HERE=`pwd`
export GOPATH=$HERE/opt/docker
mkdir -p $GOPATH/src/github.com/dotcloud
mv docker $GOPATH/src/github.com/dotcloud
cd $GOPATH/src/github.com/dotcloud/docker

export GOPATH=$HERE/opt/docker:$HERE/opt/docker/src/github.com/dotcloud/docker/vendor

# Get it with:: git rev-parse --short HEAD
export DOCKER_GITCOMMIT=c348c04
./hack/make.sh dynbinary

%install
install -Dm755 opt/docker/src/github.com/dotcloud/docker/bundles/%{version}/dynbinary/dockerinit-%{version} %{buildroot}/bin/dockerinit
install -Dm755 opt/docker/src/github.com/dotcloud/docker/bundles/%{version}/dynbinary/docker-%{version} %{buildroot}/bin/docker
install -Dm644 opt/docker/src/github.com/dotcloud/docker/contrib/completion/bash/docker %{buildroot}/usr/share/bash-completion/docker
install -Dm644 opt/docker/src/github.com/dotcloud/docker/contrib/completion/zsh/_docker %{buildroot}/usr/share/zsh/site-functions/_docker
install -Dm644 $RPM_SOURCE_DIR/dockerd.service %{buildroot}/etc/systemd/system/dockerd.service
install -Dm755 $RPM_SOURCE_DIR/docker.sysvinit %{buildroot}/etc/rc.d/init.d/docker

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/bin/docker
/bin/dockerinit
/etc/systemd/system/dockerd.service
/usr/share/bash-completion/docker
/usr/share/zsh/site-functions/_docker
/etc/rc.d/init.d/docker

%changelog
* Mon Jan 14 2014 Ben Sanchez - 0.6.4
- Initial rpm
