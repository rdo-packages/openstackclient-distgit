Name:             python-openstackclient
Version:          XXX
Release:          XXX
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
# Required to compile translation files
BuildRequires:    python-babel

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

%description
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%package doc
Summary:          Documentation for OpenStack Command-line Client

BuildRequires:    python-sphinx

Requires:         %{name} = %{version}-%{release}

%description      doc
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

# We handle requirements ourselves, pkg_resources only bring pain
rm -rf requirements.txt test-requirements.txt

%build
%{__python2} setup.py build

# Generate i18n iles
%{__python2} setup.py compile_catalog -d build/lib/openstackclient/locale

%install
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

%files -f openstackclient.lang
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
