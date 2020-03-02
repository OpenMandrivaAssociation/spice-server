%define major 1
%define Werror_cflags %nil
%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define libname %mklibname %{name} %major
%define libnamedev %mklibname %{name} -d

Name:		spice-server
Version:	0.14.3
Release:	1
Summary:	Implements the SPICE protocol
Group:		Networking/Remote access
License:	LGPLv2+
URL:		http://www.spice-space.org/
Source0:	http://www.spice-space.org/download/releases/%{name}/spice-%{version}.tar.bz2

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
ExclusiveArch:	%{ix86} %{x86_64} %{armx}

BuildRequires:	pkgconfig
BuildRequires:	spice-protocol >= 0.12.14
BuildRequires:	pixman-devel
BuildRequires:	python3dist(pyparsing)
BuildRequires:	alsa-oss-devel openssl-devel 
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(glib-2.0)
#BuildRequires:	cegui06-devel
BuildRequires:	pkgconfig(libcacard)
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

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
Requires:	pkgconfig(libcacard)
Provides:	%name-devel = %version-%release


%description -n %libnamedev
This package contains the header files, static libraries and development
documentation for spice-server. If you like to develop programs
using spice-server, you will need to install spice-server-devel.

%prep
%setup -q -n spice-%{version}
%autopatch -p1


%build
export PYTHON=%__python3
export CC=gcc
export CXX=g++
%configure --enable-smartcard --disable-werror --disable-celt051
%make_build WARN_CFLAGS='' V=1 LIBS="-lX11 -lXext -lXrandr -lXrender -lXfixes -lasound"

%install
%make_install
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la

%files -n %libname
%doc COPYING README
%{_libdir}/libspice-server.so.%{major}*

%files -n %libnamedev
%{_includedir}/spice-server
%{_libdir}/libspice-server.so
%{_libdir}/pkgconfig/spice-server.pc
