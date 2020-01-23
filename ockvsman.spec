Summary: Opencode KVS Manager
Name: ockvsman
Version: 1.0.1
Release: 8%{?dist}%{?ocrel}
BuildArch: noarch
URL: http://www.opencode.com
License: Commercial
Group: opencode
Source: ockvsman-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Packager: hristo.slavov@opencode.com
Requires: python34, python34-libs, python34-websocket-client, python34-urllib3, python34-markdown, python34-sqlalchemy, python34-click, python34-pycryptodomex, python34-jinja2, python34-markupsafe, ocpytools, python34-itsdangerous, python34-flask_restful, python34-werkzeug, python34-flask

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
mkdir -p $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/lib/
mkdir -p $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/docs/
mkdir -p $RPM_BUILD_ROOT/aux1/ockvsman/logs/
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/

cp -f lib/* $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/lib/
cp -f bin/* $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/bin/
cp -f docs/* $RPM_BUILD_ROOT/aux0/customer/containers/ockvsman/docs/

ln -sf /aux0/customer/containers/ockvsman/bin/ockvsman.py $RPM_BUILD_ROOT/usr/local/bin/ockvsman

%files
%defattr(-,root,root)
%dir /aux0/customer/containers/ockvsman/
/aux0/customer/containers/ockvsman/bin
/aux0/customer/containers/ockvsman/lib
/aux0/customer/containers/ockvsman/docs/
/aux1/ockvsman/logs/
/usr/local/bin/ockvsman

%changelog

