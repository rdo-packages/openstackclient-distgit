Name:             python-openstackclient
Version:          0.2.2
Release:          4%{?dist}
Summary:          OpenStack Command-line Client

Group:            Development/Languages
License:          ASL 2.0
URL:              http://github.com/openstack/python-openstackclient
Source0:          http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

#
# patches_base=0.2.2+1
#
Patch0001: 0001-Add-to-clientmanager-tests.patch
Patch0002: 0002-Add-object-store-show-commands.patch
Patch0003: 0003-Updated-from-global-requirements.patch
Patch0004: 0004-Add-options-to-support-TLS-certificate-verification.patch
Patch0005: 0005-Sync-oslo-incubator-for-py33-fixes.patch
Patch0006: 0006-Updated-from-global-requirements.patch
Patch0007: 0007-Do-lookups-for-user-project-in-volume-create.patch
Patch0008: 0008-Updated-from-global-requirements.patch
Patch0009: 0009-Remove-httpretty-from-test-requirements.patch
Patch0010: 0010-Update-URL-for-global-hacking-doc-and-fix-typos.patch
Patch0011: 0011-change-execute-to-run.patch
Patch0012: 0012-Complete-basic-test-infrastructure.patch
Patch0013: 0013-Add-server-image-create-command.patch
Patch0014: 0014-Support-building-wheels-PEP-427.patch
Patch0015: 0015-Fix-typo.patch

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
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1

# Remove bundled egg-info
rm -rf python_openstackclient.egg-info

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
%doc LICENSE README.rst
%{_bindir}/openstack
%{python_sitelib}/openstackclient
%{python_sitelib}/*.egg-info
%{_mandir}/man1/openstack.1*

%files doc
%doc html

%changelog
* Fri Nov 22 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.2-4
- Update with patches from upstream master

* Tue Nov 19 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.2-2
- doc subpackage now requires main package
- Use %{__python2} macro instead of %{__python}

* Wed Oct 30 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.2-1
- Initial package version based on cinderclient
