%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order whereto python-zunclient python-watcherclient python-cyborgclient
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

# Command name
%global cname openstack

# library name
%global sname %{cname}client

%global with_doc 1

%global common_desc \
python-%{sname} is a unified command-line client for the OpenStack APIs. \
It is a thin wrapper to the stock python-*client modules that implement the \
actual REST API client actions.

Name:             python-%{sname}
Version:          XXX
Release:          XXX
Summary:          OpenStack Command-line Client

License:          Apache-2.0
URL:              http://launchpad.net/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python3-%{sname}
Summary:    OpenStack Command-line Client
Obsoletes: python2-%{sname} < %{version}-%{release}

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    python3-osc-lib-tests
Requires:         python-%{sname}-lang = %{version}-%{release}
# Dependency for auto-completion
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:         bash-completion
%endif

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:          Documentation for OpenStack Command-line Client

Requires: python3-%{sname} = %{version}-%{release}

%description -n python-%{sname}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package  -n python-%{sname}-lang
Summary:   Translation files for Openstackclient

%description -n python-%{sname}-lang
Translation files for Openstackclient

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git


# (TODO) Remove this sed after fix is merged upstream
# https://review.opendev.org/c/openstack/python-openstackclient/+/808079
# Replace assertItemsEqual by assertCountEqual in test_volume_messages.py file
sed -i 's/assertItemsEqual/assertCountEqual/g' ./openstackclient/tests/unit/volume/v3/test_volume_message.py

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel


%install
%pyproject_install

# Generate i18n files
%{__python3} setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/%{sname}/locale --domain openstackclient


# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cname} %{buildroot}%{_bindir}/%{cname}-3

%if 0%{?with_doc}
export PYTHONPATH=.
%tox -e docs
sphinx-build -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/%{cname}.1 %{buildroot}%{_mandir}/man1/%{cname}.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo doc/build/html/.htaccess
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/%{sname}/locale/*/LC_*/%{sname}*po
rm -f %{buildroot}%{python3_sitelib}/%{sname}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{sname}/locale %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{python3_sitelib}/%{sname}/locale

# Find language files
%find_lang %{sname} --all-name

%post -n python3-%{sname}
mkdir -p /etc/bash_completion.d
openstack complete | sed -n '/_openstack/,$p' > /etc/bash_completion.d/osc.bash_completion

%check
export PYTHON=%{__python3}
%tox -e %{default_toxenv}

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/%{cname}
%{_bindir}/%{cname}-3
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.dist-info
%if 0%{?with_doc}
%{_mandir}/man1/%{cname}.1*

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{sname}-lang -f %{sname}.lang
%license LICENSE

%changelog
