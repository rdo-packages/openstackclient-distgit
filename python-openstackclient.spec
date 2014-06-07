Name:             python-openstackclient
Version:          0.3.1
Release:          3%{?dist}
Summary:          OpenStack Command-line Client

Group:            Development/Languages
License:          ASL 2.0
URL:              http://github.com/openstack/python-openstackclient
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

#
# patches_base=0.3.1+1
#
Patch0001: 0001-Remove-runtime-dependency-on-python-pbr.patch

BuildArch:        noarch

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1
BuildRequires:    python-sphinx

Requires:         python-pbr
Requires:         python-cliff
Requires:         python-keyring
Requires:         python-crypto
Requires:         python-glanceclient
Requires:         python-keystoneclient
Requires:         python-novaclient
Requires:         python-cinderclient
Requires:         python-six
Requires:         python-requests

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
%setup -q

%patch0001 -p1

# We provide version like this in order to remove runtime dep on pbr
sed -i s/REDHATOPENSTACKCLIENTVERSION/%{version}/ openstackclient/__init__.py

# We handle requirements ourselves, pkg_resources only bring pain
rm -rf requirements.txt test-requirements.txt

# Remove bundled egg-info
rm -rf python_openstackclient.egg-info

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
%doc LICENSE README.rst
%{_bindir}/openstack
%{python_sitelib}/openstackclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/openstack.1*

%files doc
%doc html

%changelog
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
