Name: contactsd
Version: 1.4.1
Release: 1
Summary: Telepathy <> QtContacts bridge for contacts
Group: System/Libraries
URL: https://github.com/nemomobile/contactsd
License: LGPLv2
Source0: %{name}-%{version}.tar.bz2
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(TelepathyQt4)
BuildRequires: pkgconfig(QtContacts)
# mlite required only for tests
BuildRequires: pkgconfig(mlite)
BuildRequires: pkgconfig(mlocale)
BuildRequires: pkgconfig(libmkcal)
BuildRequires: pkgconfig(telepathy-glib)

%description
contactsd is a service for collecting and observing changes in roster list
from all the users telepathy accounts (buddies, their status and presence
information), and store it to QtContacts.

%files
%defattr(-,root,root,-)
%{_libdir}/systemd/user/contactsd.service
%{_bindir}/contactsd
%{_libdir}/contactsd-1.0/plugins/*.so
# we currently don't have a backup framework
%exclude /usr/share/backup-framework/applications/contactsd.conf


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{_includedir}/contactsd-1.0/*
%dir %{_includedir}/contactsd-1.0
%{_libdir}/pkgconfig/*.pc


%package tests
Summary: Tests for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description tests
%{summary}.

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}


%prep
%setup -q -n %{name}-%{version}

%build
./configure --bindir %{_bindir} --libdir %{_libdir} --includedir %{_includedir}
%qmake
make %{?_smp_mflags}


%install
make INSTALL_ROOT=%{buildroot} install
