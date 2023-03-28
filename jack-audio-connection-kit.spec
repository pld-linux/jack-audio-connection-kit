#
# Conditional build:
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_without	cap		# don't use capabilities to get real-time priority (needs suid root binary)
%bcond_without	posix_shm	# don't use posix shm
%bcond_without	static_libs	# don't build static libs
%bcond_without	ffado		# don't build firewire (FFADO) driver
%bcond_without	freebob		# don't build freebob driver
#
Summary:	The JACK Audio Connection Kit
Summary(pl.UTF-8):	JACK - zestaw do połączeń audio
Name:		jack-audio-connection-kit
Version:	0.126.0
Release:	1
License:	LGPL v2.1+ (libjack), GPL v2+ (the rest)
Group:		Daemons
#Source0Download: https://github.com/jackaudio/jack1/releases
Source0:	https://github.com/jackaudio/jack1/releases/download/%{version}/jack1-%{version}.tar.gz
# Source0-md5:	5913c06644855f472894da53a624e63f
Patch0:		%{name}-gcc4.patch
Patch2:		link.patch
Patch3:		%{name}-update.patch
Patch4:		%{name}-man.patch
URL:		https://jackaudio.org/
BuildRequires:	alsa-lib-devel >= 1.0.18
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	celt-devel >= 0.5.0
BuildRequires:	db-devel
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_cap:BuildRequires:	libcap-devel}
%{?with_ffado:BuildRequires:	libffado-devel >= 1.999.17}
%{?with_freebob:BuildRequires:	libfreebob-devel >= 1.0.0}
BuildRequires:	libsamplerate-devel >= 0.1.2
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.98
%{?with_apidocs:BuildRequires:	texlive-pdftex}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	alsa-lib >= 1.0.18
Obsoletes:	jack-audio-connection-kit-driver-alsa < 0.101.1-2
Obsoletes:	jack-audio-connection-kit-driver-iec61883 < 0.99.0
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
License:	LGPL v2.1+
Group:		Libraries
Conflicts:	jack-audio-connection-kit < 0.100.7

%description libs
Shared JACK library.

%description libs -l pl.UTF-8
Biblioteka współdzielona JACK-a.

%package devel
Summary:	Header files for JACK
Summary(pl.UTF-8):	JACK - pliki nagłówkowe
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for the JACK Audio Connection Kit.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla zestawu do połączeń audio JACK.

%package static
Summary:	Static JACK library
Summary(pl.UTF-8):	Statyczna biblioteka JACK
License:	LGPL v2.1+
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

%package driver-firewire
Summary:	FireWire (FFADO) sound driver for JACK
Summary(pl.UTF-8):	Sterownik dźwięku FireWire (FFADO) dla JACK-a
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libffado >= 1.999.17

%description driver-firewire
FireWire (FFADO) sound driver for JACK.

%description driver-firewire -l pl.UTF-8
Sterownik dźwięku FireWire (FFADO) dla JACK-a.

%package driver-freebob
Summary:	FreeBoB sound driver for JACK
Summary(pl.UTF-8):	Sterownik dźwięku FreeBoB dla JACK-a
License:	GPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libfreebob >= 1.0.0

%description driver-freebob
FreeBoB (BeBoB platform) sound driver for JACK.

%description driver-freebob -l pl.UTF-8
Sterownik dźwięku FreeBoB (do platformy BeBoB) dla JACK-a.

%prep
%setup -q -n jack1-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--enable-dynsimd \
	%{?debug:--enable-debug} \
	--disable-coreaudio \
	%{!?with_ffado:--disable-ffado} \
	%{!?with_freebob:--disable-freebob} \
	--disable-oldtrans \
	--disable-portaudio \
	--enable-oss \
	%{?with_cap:--enable-capabilities %{!?debug:--enable-stripped-jackd}} \
	--enable-posix-shm%{!?with_posix_shm:=no} \
	%{?with_static_libs:--enable-static} \
	--enable-preemption-check \
	--enable-resize \
	--disable-silent-rules \
	--enable-timestamps \
	--with-default-tmpdir=/tmp \
	--with-html-dir=%{_gtkdocdir}/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}/%{name}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

# loadable modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/jack/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/jack/*.a
%endif

# tools/clients moved to jack-example-tools.spec
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/alsa_{in,out}.1* \
	$RPM_BUILD_ROOT%{_mandir}/man1/jack_{bufsize,connect,disconnect,freewheel,impulse_grabber,load_test,lsp,metro,monitor_client,netsource,samplerate,showtime,transport,wait}.1* \
	$RPM_BUILD_ROOT%{_mandir}/man1/jackrec.1*

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
%attr(755,root,root) %{_bindir}/jackd
%{?with_cap:%attr(4755,root,root) %{_bindir}/jackstart}
%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_alsa_midi.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_net.so
%attr(755,root,root) %{_libdir}/jack/jack_oss.so
%{_mandir}/man1/jack_iodelay.1*
%{_mandir}/man1/jack_load.1*
%{_mandir}/man1/jack_property.1*
%{_mandir}/man1/jack_unload.1*
%{_mandir}/man1/jackd.1*
%{_mandir}/man1/jackstart.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjack.so.0
%attr(755,root,root) %{_libdir}/libjackserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjackserver.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so
%attr(755,root,root) %{_libdir}/libjackserver.so
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

%if %{with ffado}
%files driver-firewire
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/jack/jack_firewire.so
%endif

%if %{with freebob}
%files driver-freebob
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/jack/jack_freebob.so
%endif
