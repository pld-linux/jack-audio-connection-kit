#
# Conditional build:
%bcond_without	apidocs		# don't generate documentation with doxygen
%bcond_without	firewire	# build FFADO driver
%bcond_without	freebob		# don't build freebob driver
%bcond_with	classic		# build also classic jackd server (see http://trac.jackaudio.org/wiki/JackDbusPackaging)
#
Summary:	The JACK Audio Connection Kit
Summary(pl.UTF-8):	JACK - zestaw do połączeń audio
Name:		jack-audio-connection-kit
Version:	1.9.7
Release:	0.4
License:	LGPL v2.1+ (libjack), GPL v2+ (the rest)
Group:		Daemons
Source0:	http://www.grame.fr/~letz/jack-%{version}.tar.bz2
# Source0-md5:	9759670feecbd43eeccf1c0f743ec199
Patch0:		jack-freebob-buildfix.patch
Patch1:		jack-doxygen-output-dirs.patch
URL:		http://jackaudio.org/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	celt-devel
BuildRequires:	dbus-devel
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_firewire:BuildRequires:	libffado-devel}
%{?with_freebob:BuildRequires:	libfreebob-devel >= 1.0.0}
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.98
%{?with_apidocs:BuildRequires:	texlive-pdftex}
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	jack-audio-connection-kit-driver-alsa
Obsoletes:	jack-audio-connection-kit-driver-iec61883
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

%description driver-freebob
FreeBoB (BeBoB platform) sound driver for JACK.

%description driver-freebob -l pl.UTF-8
Sterownik dźwięku FreeBoB (do platformy BeBoB) dla JACK-a.

%package example-clients
Summary:	Example clients that use JACK
Summary(pl.UTF-8):	Przykładowe programy kliencie używające JACK-a
License:	GPL v2+
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
License:	GPL v2+
Group:		Applications/Sound
Requires:	%{name} = %{version}-%{release}

%description example-jackrec
Example JACK client: jackrec. It's separated because it uses
libsndfile library.

%description example-jackrec -l pl.UTF-8
Przykładowy klient zestawu JACK: jackrec. Jest wydzielony, ponieważ
wymaga biblioteki libsndfile.

%prep
%setup -q -n jack-%{version}
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
export CXXFLAGS="%{rpmcxxflags} -I/usr/include/ncurses"
export CPPFLAGS="%{rpmcxxflags} -I/usr/include/ncurses"
export LINKFLAGS="%{rpmldflags}"

./waf configure \
	-v \
	%{?debug:--debug} \
	--prefix=%{_prefix} \
	--libdir=/%{_lib} \
	--libdir32=/lib \
	--dbus \
	%{?with_classic:--classic} \
	%{?with_apidocs:--doxygen} \
	%{?with_firewire:--firewire} \
	%{?with_freebob:--freebob} \
	--alsa

./waf build %{?_smp_mflags} -v

%install
rm -rf $RPM_BUILD_ROOT


HTML_DIR=%{_gtkdocdir}/%{name}/reference \
./waf install \
	--destdir=$RPM_BUILD_ROOT

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

# For compatibility with jack1
mv $RPM_BUILD_ROOT%{_bindir}/jack_rec $RPM_BUILD_ROOT%{_bindir}/jackrec

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%verifyscript libs
if ! grep -q -s '^[^ ]* /dev/shm tmpfs ' /proc/mounts ; then
	echo "/dev/shm is not mounted, but JACK requires it"
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README* TODO
%attr(755,root,root) %{_bindir}/jack_alias
%attr(755,root,root) %{_bindir}/jack_control
%attr(755,root,root) %{_bindir}/jack_cpu
%attr(755,root,root) %{_bindir}/jack_cpu_load
%attr(755,root,root) %{_bindir}/jack_evmon
%attr(755,root,root) %{_bindir}/jack_iodelay
%attr(755,root,root) %{_bindir}/jack_latent_client
%attr(755,root,root) %{_bindir}/jack_load
%attr(755,root,root) %{_bindir}/jack_midi_dump
%attr(755,root,root) %{_bindir}/jack_server_control
%attr(755,root,root) %{_bindir}/jack_session_notify
%attr(755,root,root) %{_bindir}/jack_test
%attr(755,root,root) %{_bindir}/jack_thru
%attr(755,root,root) %{_bindir}/jack_unload
%attr(755,root,root) %{_bindir}/jack_zombie
%{?with_classic:%attr(755,root,root) %{_bindir}/jackd}
%attr(755,root,root) %{_bindir}/jackdbus
%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/audioadapter.so
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_loopback.so
%attr(755,root,root) %{_libdir}/jack/jack_netone.so
%attr(755,root,root) %{_libdir}/jack/jack_net.so
%attr(755,root,root) %{_libdir}/jack/netadapter.so
%attr(755,root,root) %{_libdir}/jack/netmanager.so
%attr(755,root,root) %{_libdir}/jack/profiler.so
%{_datadir}/dbus-1/services/org.jackaudio.service
%{?with_classic:%{_mandir}/man1/jackd.1*}
%{_mandir}/man1/jack_iodelay.1*
%{_mandir}/man1/jack_load.1*
%{_mandir}/man1/jack_unload.1*

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
%{_includedir}/jack
%{_pkgconfigdir}/jack.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif

%if %{with firewire}
%files driver-firewire
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/jack/jack_firewire.so
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
%attr(755,root,root) %{_bindir}/jack_lsp
%attr(755,root,root) %{_bindir}/jack_metro
%attr(755,root,root) %{_bindir}/jack_midiseq
%attr(755,root,root) %{_bindir}/jack_midisine
%attr(755,root,root) %{_bindir}/jack_monitor_client
%attr(755,root,root) %{_bindir}/jack_multiple_metro
%attr(755,root,root) %{_bindir}/jack_netsource
%attr(755,root,root) %{_bindir}/jack_samplerate
%attr(755,root,root) %{_bindir}/jack_showtime
%attr(755,root,root) %{_bindir}/jack_simple_client
%attr(755,root,root) %{_bindir}/jack_simple_session_client
%attr(755,root,root) %{_bindir}/jack_transport
%attr(755,root,root) %{_bindir}/jack_wait
%attr(755,root,root) %{_libdir}/jack/inprocess.so
%{_mandir}/man1/alsa_in.1*
%{_mandir}/man1/alsa_out.1*
%{_mandir}/man1/jack_bufsize.1*
%{_mandir}/man1/jack_connect.1*
%{_mandir}/man1/jack_disconnect.1*
%{_mandir}/man1/jack_freewheel.1*
%{_mandir}/man1/jack_lsp.1*
%{_mandir}/man1/jack_metro.1*
%{_mandir}/man1/jack_monitor_client.1*
%{_mandir}/man1/jack_netsource.1*
%{_mandir}/man1/jack_samplerate.1*
%{_mandir}/man1/jack_showtime.1*
%{_mandir}/man1/jack_simple_client.1*
%{_mandir}/man1/jack_transport.1*
%{_mandir}/man1/jack_wait.1*

%files example-jackrec
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jackrec
%{_mandir}/man1/jackrec.1*
