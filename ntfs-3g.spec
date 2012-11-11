Summary:	Full featured NTFS driver
Name:		ntfs-3g
Version:	2012.1.15
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://tuxera.com/opensource/%{name}_ntfsprogs-%{version}.tgz
# Source0-md5:	341acae00a290cab9b00464db65015cc
URL:		http://www.ntfs-3g.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	fuse-devel
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NTFS-3G is a stable, full-featured, read-write NTFS driver for Linux,
Android, Mac OS X, FreeBSD, NetBSD, OpenSolaris, QNX, Haiku, and other
operating systems. It provides safe handling of the Windows XP,
Windows Server 2003, Windows 2000, Windows Vista, Windows Server 2008
and Windows 7 NTFS file systems.

%package libs
Summary:	libntfs-3g library
Group:		Libraries

%description libs
libntfs-3g library.

%package devel
Summary:	Header files for libntfs-3g library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package includes the header files needed to link software with
libnfts-3g libraries.

%prep
%setup -qn %{name}_ntfsprogs-%{version}

%build
%if 1
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%endif
%configure \
	--disable-ldconfig	\
	--disable-static	\
	--with-fuse=external
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# mount.ntfs-3g manpage fix
rm $RPM_BUILD_ROOT%{_mandir}/man8/mount.ntfs-3g.8
echo ".so ntfs-3g.8" > $RPM_BUILD_ROOT%{_mandir}/man8/mount.ntfs-3g.8

mv $RPM_BUILD_ROOT{/sbin/*,%{_sbindir}}

ln -s %{_bindir}/ntfs-3g $RPM_BUILD_ROOT%{_sbindir}/mount.ntfs
ln -s %{_bindir}/ntfs-3g $RPM_BUILD_ROOT%{_sbindir}/ntfsmount

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/lowntfs-3g
%attr(755,root,root) %{_bindir}/ntfs-3g
%attr(755,root,root) %{_bindir}/ntfs-3g.probe
%attr(755,root,root) %{_bindir}/ntfs-3g.secaudit
%attr(755,root,root) %{_bindir}/ntfs-3g.usermap
%attr(755,root,root) %{_bindir}/ntfscat
%attr(755,root,root) %{_bindir}/ntfscluster
%attr(755,root,root) %{_bindir}/ntfscmp
%attr(755,root,root) %{_bindir}/ntfsfix
%attr(755,root,root) %{_bindir}/ntfsinfo
%attr(755,root,root) %{_bindir}/ntfsls
%attr(755,root,root) %{_sbindir}/mkntfs
%attr(755,root,root) %{_sbindir}/ntfsclone
%attr(755,root,root) %{_sbindir}/ntfscp
%attr(755,root,root) %{_sbindir}/ntfslabel
%attr(755,root,root) %{_sbindir}/ntfsresize
%attr(755,root,root) %{_sbindir}/ntfsundelete
%attr(755,root,root) %{_sbindir}/mkfs.ntfs
%attr(755,root,root) %{_sbindir}/mount.lowntfs-3g
%attr(755,root,root) %{_sbindir}/mount.ntfs
%attr(755,root,root) %{_sbindir}/mount.ntfs-3g
%attr(755,root,root) %{_sbindir}/ntfsmount
%{_mandir}/man8/*.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libntfs-3g.so.??
%attr(755,root,root) %{_libdir}/libntfs-3g.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libntfs-3g.so
%{_libdir}/libntfs-3g.la
%{_includedir}/ntfs-3g
%{_pkgconfigdir}/libntfs-3g.pc

