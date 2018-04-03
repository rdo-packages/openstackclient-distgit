%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global client openstackclient

Name:             python-openstackclient
Version:          3.12.1
Release:          1%{?dist}
Summary:          OpenStack Command-line Client

License:          ASL 2.0
URL:              http://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

%description
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%package -n python2-%{client}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python2-%{client}}

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1
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
# Required to compile translation files
BuildRequires:    python-babel
# Required for unit tests
BuildRequires:    python-os-testr
BuildRequires:    python2-osc-lib-tests
BuildRequires:    python-coverage
BuildRequires:    python-fixtures
BuildRequires:    python-oslotest
BuildRequires:    python-reno
BuildRequires:    python-requestsexceptions
BuildRequires:    python-openstacksdk
BuildRequires:    python-osprofiler

Requires:         python-pbr
Requires:         python-babel
Requires:         python-cliff
Requires:         python-openstacksdk >= 0.9.17
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-glanceclient >= 1:2.8.0
Requires:         python-keystoneauth1 >= 3.1.0
Requires:         python-keystoneclient >= 1:3.8.0
Requires:         python-novaclient >= 1:9.0.0
Requires:         python-cinderclient >= 3.1.0
Requires:         python-neutronclient >= 6.3.0
Requires:         python-six >= 1.9.0
Requires:         python-osc-lib >= 1.7.0
Requires:         python-%{client}-lang = %{version}-%{release}


%description -n python2-%{client}
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%package -n python-%{client}-doc
Summary:          Documentation for OpenStack Command-line Client

BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme

Requires:         %{name} = %{version}-%{release}

%description -n python-%{client}-doc
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

This package contains auto-generated documentation.

%package  -n python-%{client}-lang
Summary:   Translation files for Openstackclient

%description -n python-%{client}-lang
Translation files for Openstackclient

%if 0%{?with_python3}
%package -n python3-%{client}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python3-%{client}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-d2to1
BuildRequires:    python3-oslo-sphinx
BuildRequires:    python3-six
BuildRequires:    python3-cliff
BuildRequires:    python3-oslo-i18n
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-simplejson
BuildRequires:    python3-requests
BuildRequires:    python3-glanceclient
BuildRequires:    python3-keystoneclient
BuildRequires:    python3-novaclient
BuildRequires:    python3-cinderclient
BuildRequires:    python3-neutronclient
BuildRequires:    python3-mock
BuildRequires:    python3-requests-mock
BuildRequires:    python3-os-client-config
# Required to compile translation files
BuildRequires:    python3-babel
# Required for unit tests
BuildRequires:    python3-os-testr
BuildRequires:    python3-osc-lib-tests
BuildRequires:    python3-coverage
BuildRequires:    python3-fixtures
BuildRequires:    python3-oslotest
BuildRequires:    python3-reno
BuildRequires:    python3-requestsexceptions
BuildRequires:    python3-openstacksdk
BuildRequires:    python3-osprofiler

Requires:         python3-pbr
Requires:         python3-babel
Requires:         python3-cliff
Requires:         python3-openstacksdk >= 0.9.17
Requires:         python3-oslo-i18n >= 2.1.0
Requires:         python3-oslo-utils >= 3.20.0
Requires:         python3-glanceclient >= 1:2.8.0
Requires:         python3-keystoneauth1 >= 3.1.0
Requires:         python3-keystoneclient >= 1:3.8.0
Requires:         python3-novaclient >= 1:9.0.0
Requires:         python3-cinderclient >= 3.1.
Requires:         python3-neutronclient >= 6.3.0
Requires:         python3-six >= 1.9.0
Requires:         python3-osc-lib >= 1.7.0
Requires:         python-%{client}-lang = %{version}-%{release}

%description -n python3-%{client}
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# We handle requirements ourselves, pkg_resources only bring pain
rm -rf requirements.txt test-requirements.txt

%build
%py2_build
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/openstackclient/locale

%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/openstack %{buildroot}%{_bindir}/openstack-%{python3_version}
ln -s ./openstack-%{python3_version} %{buildroot}%{_bindir}/openstack-3
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
ln -s ./openstack %{buildroot}%{_bindir}/openstack-2
ln -s ./openstack %{buildroot}%{_bindir}/openstack-%{python2_version}

%{__python2} setup.py build_sphinx -b html
%{__python2} setup.py build_sphinx -b man

install -p -D -m 644 doc/build/man/openstack.1 %{buildroot}%{_mandir}/man1/openstack.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/openstackclient/locale/*/LC_*/openstackclient*po
rm -f %{buildroot}%{python2_sitelib}/openstackclient/locale/*pot
mv %{buildroot}%{python2_sitelib}/openstackclient/locale %{buildroot}%{_datadir}/locale

%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/openstackclient/locale
%endif

# Find language files
%find_lang openstackclient --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{client}
%license LICENSE
%doc README.rst
%{_bindir}/openstack
%{_bindir}/openstack-2
%{_bindir}/openstack-%{python2_version}
%{python2_sitelib}/openstackclient
%{python2_sitelib}/*.egg-info
%{_mandir}/man1/openstack.1*

%files -n python-%{client}-doc
%license LICENSE
%doc doc/build/html

%files -n python-%{client}-lang -f openstackclient.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{client}
%license LICENSE
%doc README.rst
%{_bindir}/openstack-3
%{_bindir}/openstack-%{python3_version}
%{python3_sitelib}/openstackclient
%{python3_sitelib}/*.egg-info
%endif
%changelog
* Tue Apr 03 2018 RDO <dev@lists.rdoproject.org> 3.12.1-1
- Update to 3.12.1

* Mon Aug 21 2017 Alfredo Moralejo <amoralej@redhat.com> 3.12.0-1
- Update to 3.12.0

