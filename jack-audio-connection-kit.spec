#
# Conditional build:
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_without	cap		# don't use capabilities to get real-time priority (needs suid root binary)
%bcond_without	posix_shm	# don't use posix shm
%bcond_without	static_libs	# don't build static libs
%bcond_without	freebob		# don't build freebob driver
#
Summary:	The JACK Audio Connection Kit
Summary(pl.UTF-8):	JACK - zestaw do połączeń audio
Name:		jack-audio-connection-kit
Version:	0.118.0
Release:	1
License:	LGPL v2.1+ (libjack), GPL v2+ (the rest)
Group:		Daemons
Source0:	http://jackaudio.org/downloads/%{name}-%{version}.tar.gz
# Source0-md5:	d58e29a55f285d54e75134cec8e02a10
Patch0:		%{name}-gcc4.patch
Patch1:		%{name}-readline.patch
URL:		http://jackaudio.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_cap:BuildRequires:	libcap-devel}
%{?with_freebob:BuildRequires:	libfreebob-devel >= 1.0.0}
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.98
%{?with_apidocs:BuildRequires:	texlive-pdftex}
Obsoletes:	jack-audio-connection-kit-driver-alsa
Obsoletes:	jack-audio-connection-kit-driver-iec61883
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l pl.UTF-8
JACK to serwer dźwięku o małych opóźnieniach, napisany głównie dla
systemu operacyjnego Linux. Może przyjąć połączenia od wielu różnych
aplikacji do urządzenia dźwiękowego, a także pozwolić im na dzielenie
dźwięku pomiędzy siebie. Programy klienckie działają jako własne
procesy (tzn. normalne aplikacje) lub mogą działać wewnątrz serwera
JACK (jako wtyczki).

JACK różni się od innych serwerów dźwięku tym, że został
zaprojektowany od początku z myślą o profesjonalnej obróbce dźwięku.
Oznacza to, że skupia się na dwóch rzeczach: synchronicznym
wykonywaniu wszystkich klientów i małych opóźnieniach działania.

%package libs
Summary:	JACK library
Summary(pl.UTF-8):	Biblioteka JACK-a
License:	LGPL
Group:		Libraries
Conflicts:	jack-audio-connection-kit < 0.100.7

%description libs
Shared JACK library.

%description libs -l pl.UTF-8
Biblioteka współdzielona JACK-a.

%package devel
Summary:	Header files for JACK
Summary(pl.UTF-8):	JACK - pliki nagłówkowe
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for the JACK Audio Connection Kit.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla zestawu do połączeń audio JACK.

%package static
Summary:	Static JACK library
Summary(pl.UTF-8):	Statyczna biblioteka JACK
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static JACK library.

%description static -l pl.UTF-8
Statyczna biblioteka JACK.

%package apidocs
Summary:	JACK Audio Connection Kit API documentation
Summary(pl.UTF-8):	Dokumentacja API JACK Audio Connection Kit
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
JACK Audio Connection Kit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API JACK Audio Connection Kit.

%package driver-freebob
Summary:	FreeBoB sound driver for JACK
Summary(pl.UTF-8):	Sterownik dźwięku FreeBoB dla JACK-a
License:	GPL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description driver-freebob
FreeBoB (BeBoB platform) sound driver for JACK.

%description driver-freebob -l pl.UTF-8
Sterownik dźwięku FreeBoB (do platformy BeBoB) dla JACK-a.

%package example-clients
Summary:	Example clients that use JACK
Summary(pl.UTF-8):	Przykładowe programy kliencie używające JACK-a
License:	GPL
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description example-clients
Small example clients that use the JACK Audio Connection Kit.

%description example-clients -l pl.UTF-8
Małe, przykładowe programy klienckie, które używają zestawu do
połączeń audio JACK.

%package example-jackrec
Summary:	Example JACK client: jackrec
Summary(pl.UTF-8):	Przykładowy klient zestawu JACK: jackrec
License:	GPL
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description example-jackrec
Example JACK client: jackrec. It's separated because it uses
libsndfile library.

%description example-jackrec -l pl.UTF-8
Przykładowy klient zestawu JACK: jackrec. Jest wydzielony, ponieważ
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
	--enable-dynsimd \
	%{?debug:--enable-debug} \
	--disable-coreaudio \
	%{!?with_freebob:--disable-freebob} \
	--disable-oldtrans \
	--disable-portaudio \
	--enable-oss \
	%{?with_cap:--enable-capabilities %{!?debug:--enable-stripped-jackd}} \
	--%{?with_posix_shm:en}%{!?with_posix_shm:dis}able-posix-shm \
	%{?with_static_libs:--enable-static} \
	--enable-ensure-mlock \
	--enable-preemption-check \
	--enable-resize \
	--enable-timestamps \
	--with-default-tmpdir=/tmp \
	--with-html-dir=%{_gtkdocdir}/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}/%{name}

%{?!with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

rm -f $RPM_BUILD_ROOT%{_libdir}/jack/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with posix_shm}
%verifyscript libs
if ! grep -q -s '^[^ ]* /dev/shm tmpfs ' /proc/mounts ; then
	echo "/dev/shm is not mounted, but JACK compiled with POSIX_SHM requires it"
fi
%endif

%files
%defattr(644,root,root,755)
# note: COPYING only specifies which parts fall under GPL and LGPL
%doc AUTHORS TODO COPYING
%{?with_cap:%attr(4755,root,root) %{_bindir}/jackstart}
%attr(755,root,root) %{_bindir}/jackd
%attr(755,root,root) %{_bindir}/jack_alias
%attr(755,root,root) %{_bindir}/jack_evmon
%attr(755,root,root) %{_bindir}/jack_load
%attr(755,root,root) %{_bindir}/jack_unload
%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_net.so
%attr(755,root,root) %{_libdir}/jack/jack_oss.so
%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjack.so.0
%attr(755,root,root) %{_libdir}/libjackserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjackserver.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so
%{_libdir}/libjack.la
%{_libdir}/libjackserver.la
%{_includedir}/jack
%{_pkgconfigdir}/jack.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjack.a
%{_libdir}/libjackserver.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif

%if %{with freebob}
%files driver-freebob
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/jack/jack_freebob.so
%endif

%files example-clients
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/alsa_in
%attr(755,root,root) %{_bindir}/alsa_out
%attr(755,root,root) %{_bindir}/jack_bufsize
%attr(755,root,root) %{_bindir}/jack_connect
%attr(755,root,root) %{_bindir}/jack_disconnect
%attr(755,root,root) %{_bindir}/jack_freewheel
%attr(755,root,root) %{_bindir}/jack_impulse_grabber
%attr(755,root,root) %{_bindir}/jack_lsp
%attr(755,root,root) %{_bindir}/jack_metro
%attr(755,root,root) %{_bindir}/jack_midiseq
%attr(755,root,root) %{_bindir}/jack_midisine
%attr(755,root,root) %{_bindir}/jack_monitor_client
%attr(755,root,root) %{_bindir}/jack_netsource
%attr(755,root,root) %{_bindir}/jack_samplerate
%attr(755,root,root) %{_bindir}/jack_showtime
%attr(755,root,root) %{_bindir}/jack_simple_client
%attr(755,root,root) %{_bindir}/jack_transport
%attr(755,root,root) %{_bindir}/jack_transport_client
%attr(755,root,root) %{_bindir}/jack_wait
%attr(755,root,root) %{_libdir}/jack/inprocess.so
%attr(755,root,root) %{_libdir}/jack/intime.so

%files example-jackrec
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jackrec
