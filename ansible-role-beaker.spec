Name:       ansible-role-beaker
Version:    0.0.1
Release:    1%{?dist}
Summary:    ansible-role-beaker
License:    ASL 2.0
URL:        https://github.com/Spredzy/ansible-role-beaker
Source0:    ansible-role-beaker-%{version}.tar.gz

BuildArch:  noarch
Requires:   ansible

%description
An Ansible module for Beaker

%prep
%setup -qc

%build

%install
mkdir -p %{buildroot}%{_datadir}/ansible/roles/beaker
chmod 755 %{buildroot}%{_datadir}/ansible/roles/beaker

cp -r defaults %{buildroot}%{_datadir}/ansible/roles/beaker
cp -r handlers %{buildroot}%{_datadir}/ansible/roles/beaker
cp -r meta %{buildroot}%{_datadir}/ansible/roles/beaker
cp -r tasks %{buildroot}%{_datadir}/ansible/roles/beaker

%files
%doc README.md
%license LICENSE
%{_datadir}/ansible/roles/beaker

%changelog
* Thu Jan 31 2019 Gonéri Le Bouder <goneri@redhat.com> - 0.0.1-1
- Initial release
