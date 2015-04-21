Name:             python-openstackclient
Version:          XXX
Release:          XXX{?dist}
Summary:          OpenStack Command-line Client

Group:            Development/Languages
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

Requires:         python-pbr
Requires:         python-babel
Requires:         python-cliff
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
Requires:         python-six
Requires:         python-requests
Requires:         python-stevedore
Requires:         os-client-config

%description
python-openstackclient is a unified command-line client for the OpenStack APIs.
It is a thin wrapper to the stock python-*client modules that implement the
actual REST API client actions.

%package doc
Summary:          Documentation for OpenStack Nova API Client
Group:            Documentation

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

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/openstackclient/tests

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
%{python_sitelib}/openstackclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/openstack.1*

%files doc
%license LICENSE
%doc html

%changelog
