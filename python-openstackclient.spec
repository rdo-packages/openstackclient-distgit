Name:             python-openstackclient
Version:          1.7.1
Release:          1%{?dist}
Summary:          OpenStack Command-line Client

License:          ASL 2.0
URL:              http://github.com/openstack/%{name}
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1
BuildRequires:    python-oslo-sphinx
BuildRequires:    git
BuildRequires:    python-six
BuildRequires:    python-cliff
BuildRequires:    python-oslo-i18n
BuildRequires:    python-oslo-utils
BuildRequires:    python-simplejson
BuildRequires:    python-requests
BuildRequires:    python-glanceclient
BuildRequires:    python-keystoneclient
BuildRequires:    python-novaclient
BuildRequires:    python-cinderclient
BuildRequires:    python-neutronclient
BuildRequires:    python-mock
BuildRequires:    python-requests-mock
BuildRequires:    python-os-client-config

Requires:         python-pbr
Requires:         python-babel
Requires:         python-cliff
Requires:         python-cliff-tablib
Requires:         python-crypto
Requires:         python-oslo-config
Requires:         python-oslo-i18n
Requires:         python-oslo-utils
Requires:         python-oslo-serialization
Requires:         python-glanceclient
Requires:         python-keystoneclient
Requires:         python-novaclient
Requires:         python-cinderclient
Requires:         python-neutronclient
Requires:         python-six >= 1.9.0
Requires:         python-requests >= 2.5.2
Requires:         python-stevedore
Requires:         python-os-client-config

%description
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%package doc
Summary:          Documentation for OpenStack Nova API Client

BuildRequires:    python-sphinx

Requires:         %{name} = %{version}-%{release}

%description      doc
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

This package contains auto-generated documentation.


%prep
%setup -q

# We handle requirements ourselves, pkg_resources only bring pain
rm -rf requirements.txt test-requirements.txt

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 man/openstack.1 %{buildroot}%{_mandir}/man1/openstack.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%license LICENSE
%doc README.rst
%{_bindir}/openstack
%{python2_sitelib}/openstackclient
%{python2_sitelib}/*.egg-info
%{_mandir}/man1/openstack.1*

%files doc
%license LICENSE
%doc html

%changelog
* Fri Oct 02 2015 Haikel Guemar <hguemar@fedoraproject.org> 1.7.1-1
- Update to upstream 1.7.1

* Mon Sep 21 2015 Alan Pevec <alan.pevec@redhat.com> 1.6.0-1
- Update to upstream 1.6.0

* Mon Jul 27 2015 Parag Nemade <pnemade AT fedoraproject DOT org> 1.5.0-1
- Update to upstream 1.5.0
- Drop upstream patch

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Jakub Ruzicka <jruzicka@redhat.com> 1.0.3-2
- Give up nuking pbr
- Add the ability to set and unset flavor properties
- Use %license

* Tue Mar 31 2015 Jakub Ruzicka <jruzicka@redhat.com> 1.0.3-1
- Update to upstream 1.0.3

* Wed Dec 10 2014 Jakub Ruzicka <jruzicka@redhat.com> 1.0.1-1
- Update to upstream 1.0.1

* Fri Sep 26 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.4.1-1
- Update to upstream 0.4.1
- New Requires: python-neutronclient, python-oslo-sphinx
- Removed Requires: python-keyring, python-sphinx
- oslosphinx -> oslo.sphinx

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 08 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-2
- Fix version info

* Tue Apr 08 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.3.1-1
- Update to upstream 0.3.1
- Remove runtime dependency on python-pbr

* Wed Jan 08 2014 Jakub Ruzicka <jruzicka@redhat.com> 0.3.0-1
- Update to upstream 0.3.0
- New dependencies: python-six, python-requests

* Fri Nov 22 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.2-4
- Update with patches from upstream master

* Tue Nov 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.2-2
- doc subpackage now requires main package
- Use %{__python2} macro instead of %{__python}

* Wed Oct 30 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.2-1
- Initial package version based on cinderclient
