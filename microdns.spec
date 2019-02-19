#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Minimal mDNS resolver (and announcer) library
Summary(pl.UTF-8):	Minimalna biblioteka do rozwiązywania (i rozgłaszania) mDNS
Name:		microdns
Version:	0.0.10
Release:	1
License:	LGPL v2.1 or commercial
Group:		Libraries
#Source0Download: https://github.com/videolabs/libmicrodns/releases
Source0:	https://github.com/videolabs/libmicrodns/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f49c39e94afc0ced59aeff94d9b76a3e
URL:		https://github.com/videolabs/libmicrodns
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Minimal mDNS resolver (and announcer) library.

%description -l pl.UTF-8
Minimalna biblioteka do rozwiązywania (i rozgłaszania) mDNS.

%package devel
Summary:	Header files for microdns library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki microdns
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for microdns library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki microdns.

%package static
Summary:	Static microdns library
Summary(pl.UTF-8):	Statyczna biblioteka microdns
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static microdns library.

%description static -l pl.UTF-8
Statyczna biblioteka microdns.

%prep
%setup -q

%{__sed} -ne '1p' COPYING > LICENSE

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies, obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmicrodns.la
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/microdns/README.md

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS README.md
%attr(755,root,root) %{_libdir}/libmicrodns.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmicrodns.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmicrodns.so
%{_includedir}/microdns
%{_pkgconfigdir}/microdns.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmicrodns.a
%endif
