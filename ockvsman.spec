Summary: Opencode KVS Manager
Name: ockvsman
Version: 1.1.1
Release: 2%{?dist}%{?ocrel}
BuildArch: noarch
URL: http://www.opencode.com
License: Commercial
Group: opencode
Source: ockvsman-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Packager: petar.kolev@opencode.com


%if 0%{?rhel} >= 8
Requires: python3, python3-libs, python3-websocket-client, python3-urllib3, python3-sqlalchemy, python3-click, python3-pycryptodomex, python3-jinja2, python3-markupsafe, ocpytools, python3-itsdangerous, python36-flask_restful, python3-werkzeug, python3-flask, python3-requests
%else
Requires: python36, python36-libs, python36-websocket-client, python36-urllib3, python36-sqlalchemy, python36-click, python36-pycryptodomex, python36-jinja2, python36-markupsafe, ocpytools, python36-itsdangerous, python36-flask_restful, python36-werkzeug, python36-flask, python36-requests
%endif


%description
Opencode KVS manager

GIT commit

Contact: petar.kolev@opencode.com

%prep
%setup -q

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt/containers/ockvsman/bin/
mkdir -p $RPM_BUILD_ROOT/opt/containers/ockvsman/bin/templates/
mkdir -p $RPM_BUILD_ROOT/opt/containers/ockvsman/lib/
mkdir -p $RPM_BUILD_ROOT/aux1/ockvsman/logs/
mkdir -p $RPM_BUILD_ROOT/usr/local/bin/

cp -f lib/* $RPM_BUILD_ROOT/opt/containers/ockvsman/lib/
cp -fr bin/* $RPM_BUILD_ROOT/opt/containers/ockvsman/bin/

ln -sf /opt/containers/ockvsman/bin/ockvsman.py $RPM_BUILD_ROOT/usr/local/bin/ockvsman

%files
%defattr(-,root,root)
%dir /opt/containers/ockvsman/
/opt/containers/ockvsman/bin
/opt/containers/ockvsman/lib
/opt/containers/ockvsman/bin/templates/
/aux1/ockvsman/logs/
/usr/local/bin/ockvsman



%preun
/usr/local/bin/ockvsman stop


%changelog
* Thu Sep 24 2020 Petar Kolev <petar.kolev@opencode.com> 1.1.1-2 
- Bug fix in stop function, that ockvsman can be removed properly if it is not running,
adding python36-requests,python3-requests to "Required" in spec

* Thu Sep 17 2020 Petar Kolev <petar.kolev@opencode.com> 1.1.1-1 
- Adding "ockvsman import etcd_fullpath_key etcd_fullpath_file" command line functionallity,
Making package to be compatible with RedHat8

* Thu July 16 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.2-1 
- (127c898b1) Reorganizing ockvsman

* Mon Apr 13 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.1-12 
- (1e66a60) Adding /getPlatformNodes url

* Fri Apr 03 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.1-11 
- (8adcb6e) Removing logic for nodes_manager url ref by M1686613 from T090563

* Thu Mar 26 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.1-11 
- (c4613e7) Adding changes

* Fri Feb 28 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.1-11 
- (8c9a0c2) Updating ...

* Thu Feb 27 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.1-11 
- (9e68b56) Updating kvs_manager

* Tue Feb 25 2020 Petar Kolev <petar.kolev@opencode.com> 1.0.1-11 
- (d04c931) Initializing new design of kvs_manager

* Thu Dec 12 2019 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (62141e7) Adding request to ockvsman POST http://0.0.0.0:9002/getkey to get value of key from etcd key value store ref by T106515

* Thu Dec 12 2019 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (7c93d6a) Adding request to ockvsman POST http://0.0.0.0:9002/getkey to get value of key from etcd key value store ref by T106515 (origin/T106515)

* Thu Feb 07 2019 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (f73624e) Adding ockvsman.py shell for start/stop/status of kvs_wrapper.py ref by T999999

* Tue Jan 15 2019 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (7d12d12) Bumping release ref by T090563

* Fri Dec 14 2018 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (dbf98e7) Fixing some bugs

* Fri Dec 14 2018 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (35e1682) Adding logging functionality to thr package

* Mon Dec 03 2018 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (8cb4efe) Fixing spec file

* Mon Dec 03 2018 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (37e50de) Fixing spec file

* Mon Dec 03 2018 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (b877fba) Fixing spec file

* Thu Nov 29 2018 Hristo Slavov <hristo.slavov@opencode.com> 1.0.1-8 
- (59820f0) Added changelog, gen_tarball, etc

* Thu Nov 29 2018 Hristo Slavov <hristo.slavov@opencode.com> 1.0.1-8 
- (cc7526f) Added .spec file

* Tue Nov 27 2018 Petar Kolev <petar.kolev@opencode.com> 1.0.1-8 
- (3ad951f) First release of ockvsman package
