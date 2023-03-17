# grreader.spec

Summary: HTML-Based RSS Reader inspired by widely known discontinued reader
URL: http://hylom.net/grrreader
Name: grrreader
Version: 0.0.7
Group: Applications/Internet
Release: 2
License: GPLv2
Source0: http://hylom.net/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: nodejs >= 0.8.0
Requires: python >= 2.6.6
Requires: python-dateutil >= 1.4.1
Requires: python-feedparser >= 5.1.2
#Requires: /usr/bin/forever
Requires: bash

%description
Grrreader is HTML and Ajax based RSS Reader application based on Node.js and Python.

%prep
%setup
sed -i -e 's/^TARGET_SCRIPT.*$/TARGET_SCRIPT=\/usr\/share\/grrreader\/client\/app.js/' initscript 


%build
cd client; npm install

%install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/grrreader
cp -pr backend ${RPM_BUILD_ROOT}%{_datadir}/grrreader/
cp -pr client ${RPM_BUILD_ROOT}%{_datadir}/grrreader/
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d
install -m 755 initscript ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/grrreader
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.d
install -m 644 cron ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.d/grrreader

%clean
rm -rf ${RPM_BUILD_ROOT}

%preun
/etc/init.d/grrreader stop

%files
%defattr(-, root, root, -)
%doc README.md
%doc license.txt
%{_datadir}/grrreader/backend
%{_datadir}/grrreader/client
%{_sysconfdir}/init.d/grrreader
%{_sysconfdir}/cron.d/grrreader

%changelog
* Wed Jun 17 2015 Hiromichi Matsushima <hylom at hylom.net> - 0.0.7-2
 - fix error exit when invalid URL in RSS

* Mon Dec 9 2013 Hiromichi Matsushima <hylom at hylom.net> - 0.0.7-1
 - fix: when invalid timestamp in RSS, replace to current timestamp

* Tue Jul 16 2013 Hiromichi Matsushima <hylom at hylom.net> - 0.0.6-1
- update to 0.0.6

* Tue Jul 16 2013 Hiromichi Matsushima <hylom at hylom.net> - 0.0.5-1
- Create RPM package

