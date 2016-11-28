%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global client python-openstackclient
%global sclient openstackclient

Name:             python-openstackclient
Version:          XXX
Release:          XXX
Summary:          OpenStack Command-line Client

License:          ASL 2.0
URL:              http://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

%package -n python2-%{sclient}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python2-%{sclient}}

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
Requires:         python-crypto
Requires:         python-openstacksdk
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
Requires:         python-osc-lib

%description -n python2-%{sclient}
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%package -n python-%{sclient}-doc
Summary:          Documentation for OpenStack Command-line Client

BuildRequires:    python-sphinx

Requires:         %{name} = %{version}-%{release}

%description -n python-%{sclient}-doc
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

This package contains auto-generated documentation.

%if 0%{?with_python3}
%package -n python3-%{sclient}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python3-%{sclient}}

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
# There is a binary conflict between python2-osprofiler (from RDO Trunk)
# and python3-osprofiler (from Fedora Rawhide)
#BuildRequires:    python3-osprofiler

Requires:         python3-pbr
Requires:         python3-babel
Requires:         python3-cliff
Requires:         python3-crypto
Requires:         python3-openstacksdk
Requires:         python3-oslo-config
Requires:         python3-oslo-i18n
Requires:         python3-oslo-utils
Requires:         python3-oslo-serialization
Requires:         python3-glanceclient
Requires:         python3-keystoneclient
Requires:         python3-novaclient
Requires:         python3-cinderclient
Requires:         python3-neutronclient
Requires:         python3-six >= 1.9.0
Requires:         python3-requests >= 2.5.2
Requires:         python3-stevedore
Requires:         python3-os-client-config
Requires:         python3-osc-lib

%description -n python3-%{sclient}
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.
%endif

%description
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# We handle requirements ourselves, pkg_resources only bring pain
rm -rf requirements.txt test-requirements.txt

%build
%{__python2} setup.py build
# Generate i18n iles
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

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html
sphinx-build -b man doc/source man

install -p -D -m 644 man/openstack.1 %{buildroot}%{_mandir}/man1/openstack.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/openstackclient/locale/*/LC_*/openstackclient*po
rm -f %{buildroot}%{python2_sitelib}/openstackclient/locale/*pot
mv %{buildroot}%{python2_sitelib}/openstackclient/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang openstackclient --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{sclient} -f openstackclient.lang
%license LICENSE
%doc README.rst
%{_bindir}/openstack
%{python2_sitelib}/openstackclient
%{python2_sitelib}/*.egg-info
%{_mandir}/man1/openstack.1*
%if 0%{?with_python3}
%exclude %{python3_sitelib}/openstackclient
%endif

%files -n python-%{sclient}-doc
%license LICENSE
%doc html

%if 0%{?with_python3}
%files -n python3-%{sclient} -f openstackclient.lang
%license LICENSE
%doc README.rst
%{_bindir}/openstack-3
%{_bindir}/openstack-%{python3_version}
%{python3_sitelib}/openstackclient
%exclude %{python2_sitelib}/openstackclient
%{python3_sitelib}/*.egg-info
%endif
%changelog
