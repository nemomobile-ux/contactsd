Name: contactsd
Version: 1.4
Release: 1
Summary: Telepathy <> QtContacts bridge for contacts
Group: System/Libraries
URL: https://git.merproject.org/mer-core/contactsd
License: LGPLv2.1+ and (LGPLv2.1 or LGPLv2.1 with Nokia Qt LGPL Exception v1.1)
Source0: %{name}-%{version}.tar.bz2
Source1: %{name}.privileges
Requires: systemd
Requires: systemd-user-session-targets
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(TelepathyQt5)
BuildRequires: pkgconfig(Qt5Versit)
# mlite required only for tests
BuildRequires: pkgconfig(mlite5)
BuildRequires: pkgconfig(mlocale5)
BuildRequires: pkgconfig(libmkcal-qt5)
BuildRequires: pkgconfig(libkcalcoren-qt5)
BuildRequires: pkgconfig(telepathy-glib)
BuildRequires: pkgconfig(qofono-qt5)
BuildRequires: pkgconfig(qofonoext)
BuildRequires: pkgconfig(qtcontacts-sqlite-qt5-extensions) >= 0.1.64
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig(gio-2.0)
# pkgconfig(buteosyncfw5) is not correctly versioned, use the provider package instead:
#BuildRequires: pkgconfig(buteosyncfw5) >= 0.6.33
BuildRequires: buteo-syncfw-qt5-devel >= 0.6.33
BuildRequires: pkgconfig(qt5-boostable)
BuildRequires: qt5-qttools
BuildRequires: qt5-qttools-linguist
Requires: libqofono-qt5 >= 0.67
Requires: mapplauncherd-qt5
#Because pkgconfig QtContacts always return 5.0.0 use packages version
BuildRequires:  qt5-qtpim-contacts-devel >= 5.8
Requires: qt5-qtpim-contacts >= 5.8

%description
%{name} is a service for collecting and observing changes in roster list
from all the users telepathy accounts (buddies, their status and presence
information), and store it to QtContacts.

%files
%defattr(-,root,root,-)
%{_libdir}/systemd/user/%{name}.service
%{_libdir}/systemd/user/post-user-session.target.wants/%{name}.service
%{_bindir}/%{name}
%{_libdir}/%{name}-1.0
%{_datadir}/translations/*.qm
%{_datadir}/mapplauncherd/privileges.d/*
# we currently don't have a backup framework
%exclude /usr/share/backup-framework/applications/%{name}.conf


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}.

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}-1.0
%{_libdir}/pkgconfig/*.pc


%package tests
Summary: Tests for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: blts-tools

%description tests
%{summary}.

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}

%package ts-devel
Summary: Translation source for %{name}
Group: Development/Languages

%description ts-devel
Translation source for %{name}

%files ts-devel
%defattr(-,root,root,-)
%{_datadir}/translations/source/*.ts


%prep
%setup -q -n %{name}-%{version}

%build
export QT_SELECT=5
export VERSION=%{version}
./configure --bindir %{_bindir} --libdir %{_libdir} --includedir %{_includedir}
%qmake5
make %{?_smp_mflags}


%install
%qmake5_install

mkdir -p %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants
ln -s ../%{name}.service %{buildroot}%{_libdir}/systemd/user/post-user-session.target.wants/

mkdir -p %{buildroot}%{_datadir}/mapplauncherd/privileges.d
install -m 644 -p %{SOURCE1} %{buildroot}%{_datadir}/mapplauncherd/privileges.d

%post
if [ "$1" -ge 1 ]; then
systemctl-user daemon-reload || :
systemctl-user try-restart %{name}.service || :
fi

%postun
if [ "$1" -eq 0 ]; then
systemctl-user stop %{name}.service || :
systemctl-user daemon-reload || :
fi

