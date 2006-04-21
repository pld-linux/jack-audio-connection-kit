#
# Conditional build:
%bcond_without	cap		# don't use capabilities to get real-time priority (needs suid root binary)
%bcond_without	posix_shm	# don't use posix shm
%bcond_without	static_libs	# don't build static libs
#
Summary:	The JACK Audio Connection Kit
Summary(pl):	JACK - zestaw do po³±czeñ audio
Name:		jack-audio-connection-kit
Version:	0.101.1
Release:	2
License:	LGPL v2.1+ (libjack), GPL v2+ (the rest)
Group:		Daemons
Source0:	http://dl.sourceforge.net/jackit/%{name}-%{version}.tar.gz
# Source0-md5:	bb25f7c1da5d488b70edcf39ff5a39b2
Patch0:		%{name}-optimized-cflags.patch
Patch1:		%{name}-gcc4.patch
URL:		http://jackit.sourceforge.net/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	doxygen
%{?with_cap:BuildRequires:	libcap-devel}
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.98
Obsoletes:	jack-audio-connection-kit-driver-alsa
Obsoletes:	jack-audio-connection-kit-driver-iec61883
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32		-fomit-frame-pointer -ffast-math
%define		specflags_pentium3	-mfpmath=sse
%define		specflags_pentium4	-mfpmath=sse
%define		specflags_x86_64	-ffast-math

%description
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (ie. as a
normal application), or can they can run within a JACK server (ie. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.

%description -l pl
JACK to serwer d¼wiêku o ma³ych opó¼nieniach, napisany g³ównie dla
systemu operacyjnego Linux. Mo¿e przyj±æ po³±czenia od wielu ró¿nych
aplikacji do urz±dzenia d¼wiêkowego, a tak¿e pozwoliæ im na dzielenie
d¼wiêku pomiêdzy siebie. Programy klienckie dzia³aj± jako w³asne
procesy (tzn. normalne aplikacje) lub mog± dzia³aæ wewn±trz serwera
JACK (jako wtyczki).

JACK ró¿ni siê od innych serwerów d¼wiêku tym, ¿e zosta³
zaprojektowany od pocz±tku z my¶l± o profesjonalnej obróbce d¼wiêku.
Oznacza to, ¿e skupia siê na dwóch rzeczach: synchronicznym
wykonywaniu wszystkich klientów i ma³ych opó¼nieniach dzia³ania.

%package libs
Summary:	JACK library
Summary(pl):	Biblioteka JACK-a
License:	LGPL
Group:		Libraries
Conflicts:	jack-audio-connection-kit < 0.100.7

%description libs
Shared JACK library.

%description libs -l pl
Biblioteka wspó³dzielona JACK-a.

%package devel
Summary:	Header files for JACK
Summary(pl):	JACK - pliki nag³ówkowe
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for the JACK Audio Connection Kit.

%description devel -l pl
Pliki nag³ówkowe dla zestawu do po³±czeñ audio JACK.

%package static
Summary:	Static JACK library
Summary(pl):	Statyczna biblioteka JACK
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static JACK library.

%description static -l pl
Statyczna biblioteka JACK.

%package example-clients
Summary:	Example clients that use JACK
Summary(pl):	Przyk³adowe programy kliencie u¿ywaj±ce JACK-a
License:	GPL
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description example-clients
Small example clients that use the JACK Audio Connection Kit.

%description example-clients -l pl
Ma³e, przyk³adowe programy klienckie, które u¿ywaj± zestawu do
po³±czeñ audio JACK.

%package example-jackrec
Summary:	Example JACK client: jackrec
Summary(pl):	Przyk³adowy klient zestawu JACK: jackrec
License:	GPL
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description example-jackrec
Example JACK client: jackrec. It's separated because it uses
libsndfile library.

%description example-jackrec
Przyk³adowy klient zestawu JACK: jackrec. Jest wydzielony, poniewa¿
wymaga biblioteki libsndfile.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoheader}
%{__automake}
%{__autoconf}

%configure \
	%{?debug:--enable-debug} \
	--disable-coreaudio \
	--disable-oldtrans \
	--disable-portaudio \
	--enable-oss \
	%{?with_cap:--enable-capabilities %{!?debug:--enable-stripped-jackd}} \
	--%{?with_posix_shm:en}%{!?with_posix_shm:dis}able-posix-shm \
	%{?with_static_libs:--enable-static} \
%ifarch athlon pentium3 pentium4 %{x8664}
	--enable-mmx \
%else
	--disable-mmx \
%endif
%ifarch pentium3 pentium4 %{x8664}
	--enable-sse \
%else
	--disable-sse \
%endif
%ifarch ppc
	--enable-altivec \
%else
	--disable-altivec \
%endif
	--enable-ensure-mlock \
	--enable-preemption-check \
	--enable-resize \
	--enable-timestamps \
	--with-default-tmpdir=/tmp \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

rm -f $RPM_BUILD_ROOT%{_libdir}/jack/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# note: COPYING only specifies which parts fall under GPL and LGPL
%doc AUTHORS TODO COPYING
%{?with_cap:%attr(4755,root,root) %{_bindir}/jackstart}
%attr(755,root,root) %{_bindir}/jackd
%attr(755,root,root) %{_bindir}/jack_load
%attr(755,root,root) %{_bindir}/jack_unload
%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_oss.so
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so
%{_libdir}/libjack.la
%{_includedir}/jack
%{_pkgconfigdir}/jack.pc
%{_gtkdocdir}/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjack.a
%endif

%files example-clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jack_bufsize
%attr(755,root,root) %{_bindir}/jack_connect
%attr(755,root,root) %{_bindir}/jack_disconnect
%attr(755,root,root) %{_bindir}/jack_freewheel
%attr(755,root,root) %{_bindir}/jack_impulse_grabber
%attr(755,root,root) %{_bindir}/jack_lsp
%attr(755,root,root) %{_bindir}/jack_metro
%attr(755,root,root) %{_bindir}/jack_monitor_client
%attr(755,root,root) %{_bindir}/jack_showtime
%attr(755,root,root) %{_bindir}/jack_simple_client
%attr(755,root,root) %{_bindir}/jack_transport
%attr(755,root,root) %{_libdir}/jack/inprocess.so
%attr(755,root,root) %{_libdir}/jack/intime.so

%files example-jackrec
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jackrec
