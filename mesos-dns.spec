%define debug_package %{nil}

Name:          mesos-dns
Version:       0.1.2
Release:       0%{?dist}
Summary:       DNS-based service discovery for Apache Mesos.
License:       ASL 2.0
URL:           http://mesosphere.github.io/mesos-dns/

Source0:       https://github.com/mesosphere/mesos-dns/archive/v%{version}.tar.gz
Source1:       %{name}.service

####################################

BuildRequires: golang >= 1.4
BuildRequires: git

%description
Mesos-DNS supports service discovery in Apache Mesos clusters.
It allows applications and services running on Mesos to find each other
through the domain name system (DNS), similarly to how services discover
each other throughout the Internet.

##############################################

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p ./_build/src/github.com/mesosphere
ln -s $(pwd) ./_build/src/github.com/mesosphere/mesos-dns

export GOPATH=$(pwd)/_build:%{gopath}
go get github.com/tools/godep
pushd ./_build/src/github.com/tools/godep
go build -o godep
popd
export PATH="$(pwd)/_build/src/github.com/tools/godep:$PATH"
make restoredeps
make build

%check

%install
install -d %{buildroot}%{_sbindir}
install -p -m 0755 ./mesos-dns %{buildroot}%{_sbindir}/mesos-dns

mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 ./config.json.sample %{buildroot}%{_sysconfdir}/%{name}/config.json

############################################
%files
%doc LICENSE README.md
%{_sbindir}/mesos-dns
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_unitdir}/%{name}.service

%pre

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Wed May  6 2015 Lukas Loesche <lukas@mesosphere.io> - 0.1.2-0.1
- Initial release
