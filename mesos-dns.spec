Name:          mesos-dns
Version:       0.1.2
Release:       1
Summary:       DNS-based service discovery for Apache Mesos.
License:       ASL 2.0
URL:           http://mesosphere.github.io/mesos-dns/

Source0:       https://github.com/mesosphere/mesos-dns/archive/v%{version}.tar.gz
Source1:       %{name}.service

####################################

BuildRequires: systemd
BuildRequires: golang


%description
Mesos-DNS supports service discovery in Apache Mesos clusters.
It allows applications and services running on Mesos to find each other
through the domain name system (DNS), similarly to how services discover
each other throughout the Internet.

##############################################

%prep
%setup -q -n %{name}-%{version}

%build
#todo

%check
#todo

%install
#todo

# system integration sysconfig setting
mkdir -p %{buildroot}%{_sysconfdir}/%{name}


############################################
%files
%doc LICENSE NOTICE
%{_sbindir}/mesos-*
#system integration files
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}*
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
