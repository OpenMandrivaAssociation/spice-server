%define major 1
%define Werror_cflags %nil

%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} -d

Name:		spice-server
Version:	0.12.0
Release:	%mkrel 1
Summary:	Implements the SPICE protocol
Group:		Networking/Remote access
License:	LGPLv2+
URL:		http://www.spice-space.org/
Source0:	http://www.spice-space.org/download/releases/spice-%{version}.tar.bz2
Source1:	spice-xpi-client-spicec

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	pkgconfig
BuildRequires:	spice-protocol >= 0.9.1
BuildRequires:	celt051-devel
BuildRequires:	pixman-devel
BuildRequires:	pythonegg(pyparsing)
BuildRequires:	alsa-oss-devel openssl-devel libjpeg-devel
BuildRequires:	pkgconfig(xrandr)
#BuildRequires:	cegui06-devel
BuildRequires:	libcacard-devel
BuildRequires:	libsasl2-devel
BuildRequires:	pkgconfig(xfixes)

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

%package client
Summary:	Implements the client side of the SPICE protocol
Group:		Networking/Remote access
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description client
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the SPICE client application.

%package -n %libname
Summary:	Implements the server side of the SPICE protocol
Group:		System/Libraries

%description -n %libname
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the run-time libraries for any application that wishes
to be a SPICE server.

%package -n %libnamedev
Summary:	Header files, libraries and development documentation for spice-server
Group:		Development/C
Requires:	%libname = %{version}-%{release}
Requires:	pkgconfig
Provides:	%name-devel = %version-%release


%description -n %libnamedev
This package contains the header files, static libraries and development
documentation for spice-server. If you like to develop programs
using spice-server, you will need to install spice-server-devel.

%prep
%setup -q -n spice-%{version}
#% patch9 -p1
#% patch10 -p1


%build
autoreconf -ifv
%configure2_5x --enable-smartcard --disable-werror
make -C spice-common WARN_CFLAGS='' %{?_smp_mflags}
make -C client WARN_CFLAGS='' %{?_smp_mflags}
%make LIBS="-lpthread"

%install
make DESTDIR=%{buildroot} -C client install
%makeinstall_std
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la
mkdir -p %{buildroot}%{_libexecdir}
touch %{buildroot}%{_libexecdir}/spice-xpi-client
install -m 0755 %{SOURCE1} %{buildroot}%{_libexecdir}/

%files client
%doc COPYING README NEWS
%{_bindir}/spicec
%ghost %{_libexecdir}/spice-xpi-client
%{_libexecdir}/spice-xpi-client-spicec

%post client
%{_sbindir}/update-alternatives --install %{_libexecdir}/spice-xpi-client \
  spice-xpi-client %{_libexecdir}/spice-xpi-client-spicec 10

%postun client
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove spice-xpi-client %{_libexecdir}/spice-xpi-client-spicec
fi

%files -n %libname
%doc COPYING README NEWS
%{_libdir}/libspice-server.so.%{major}*

%files -n %libnamedev
%{_includedir}/spice-server
%{_libdir}/libspice-server.so
%{_libdir}/pkgconfig/spice-server.pc
