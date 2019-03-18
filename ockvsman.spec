Summary: Opencode KVS Manager
Name: ockvsman
Version: 1.0.1
Release: 6%{?dist}%{?ocrel}
BuildArch: noarch
URL: http://www.opencode.com
License: Commercial
Group: opencode
Source: ockvsman-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Packager: hristo.slavov@opencode.com
Requires: python34, docker-ce, python34-libs, python34-websocket-client, python34-urllib3, ocpytools

%description
Opencode KVS manager

GIT commit

Contact: hristo.slavov@opencode.com

%prep
%setup -q

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/bin/
mkdir -p $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/etc/
mkdir -p $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/lib/
mkdir -p $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/run/
mkdir -p $RPM_BUILD_ROOT/aux1/ockvsman/logs/
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/

cp -f lib/* $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/lib/
cp -f bin/* $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/bin/

ln -sf /aux0/customer/containers/ockvsman/bin/ockvsman.py $RPM_BUILD_ROOT/usr/local/bin/ockvsman

%files
%defattr(-,root,root)
%dir /aux0/customer/containers/ockvsman/
/aux0/customer/containers/ockvsman/bin
/aux0/customer/containers/ockvsman/etc
/aux0/customer/containers/ockvsman/lib
/aux0/customer/containers/ockvsman/run
/aux1/ockvsman/logs/
/usr/local/bin/ockvsman

%changelog

