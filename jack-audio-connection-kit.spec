# TODO: --iio (BR: gtkIOStream >= 1.4.0, eigen3 >= 3.1.2)
#
# Conditional build:
%bcond_without	apidocs		# Doxygen docs
%bcond_without	ffado		# firewire (FFADO) driver
%bcond_with	classic		# build also classic jackd server (see http://trac.jackaudio.org/wiki/JackDbusPackaging)

Summary:	The JACK Audio Connection Kit
Summary(pl.UTF-8):	JACK - zestaw do połączeń audio
Name:		jack-audio-connection-kit
Version:	1.9.22
Release:	1
License:	LGPL v2.1+ (libjack), GPL v2+ (the rest)
Group:		Daemons
#Source0Download: https://jackaudio.org/downloads/
#Source0:	https://github.com/jackaudio/jack2/releases/download/v%{version}/jack2-%{version}.tar.gz
Source0:	https://github.com/jackaudio/jack2/archive/v%{version}/jack2-%{version}.tar.gz
# Source0-md5:	e57c8ad3de75f78b6eb7aacea4e25755
URL:		https://jackaudio.org/
BuildRequires:	alsa-lib-devel >= 1.0.18
BuildRequires:	celt-devel >= 0.11.0
BuildRequires:	dbus-devel >= 1.0.0
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel
%{?with_ffado:BuildRequires:	libffado-devel >= 1.999.17}
BuildRequires:	libsamplerate-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
# with opus_custom interface
BuildRequires:	opus-devel >= 1.0.3-2
%{?with_apidocs:BuildRequires:	texlive-pdftex}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	alsa-lib >= 1.0.18
Obsoletes:	jack-audio-connection-kit-driver-alsa < 0.101.1-2
Obsoletes:	jack-audio-connection-kit-driver-iec61883 < 0.99.0
Obsoletes:	jack-audio-connection-kit-example-jackrec < 1.9.22
Obsoletes:	jack-audio-connection-kit-static < 1.9.7
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
Requires:	celt >= 0.11.0
Requires:	dbus-libs >= 1.0.0
Requires:	opus >= 1.0.3-2
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

%package apidocs
Summary:	JACK Audio Connection Kit API documentation
Summary(pl.UTF-8):	Dokumentacja API JACK Audio Connection Kit
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

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
Obsoletes:	jack-driver-freebob < 1.9.13

%description driver-firewire
FireWire (FFADO) sound driver for JACK.

%description driver-firewire -l pl.UTF-8
Sterownik dźwięku FireWire (FFADO) dla JACK-a.

%prep
%setup -q -n jack2-%{version}

%build
export CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
export CXXFLAGS="%{rpmcxxflags} -I/usr/include/ncurses"
export CPPFLAGS="%{rpmcxxflags} -I/usr/include/ncurses"
export LINKFLAGS="%{rpmldflags}"

./waf configure -j1 \
	-v \
	%{?debug:--debug} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--htmldir=%{_gtkdocdir}/%{name}/reference \
	--alsa \
	%{?with_classic:--classic} \
	--dbus \
	%{?with_apidocs:--doxygen} \
	%{?with_ffado:--firewire}

./waf build %{?_smp_mflags} -v

%install
rm -rf $RPM_BUILD_ROOT

./waf install \
	--destdir=$RPM_BUILD_ROOT

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

# not built or packaged
%if %{without classic}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/jackd.1
%endif

# fix perms (needed for autorequires/provides)
chmod a+x $RPM_BUILD_ROOT%{_libdir}/lib*.so*
chmod a+x $RPM_BUILD_ROOT%{_libdir}/jack/*.so

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
%doc AUTHORS.rst ChangeLog.rst README*
%attr(755,root,root) %{_bindir}/jack_control
%{?with_classic:%attr(755,root,root) %{_bindir}/jackd}
%attr(755,root,root) %{_bindir}/jackdbus
%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/audioadapter.so
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_alsarawmidi.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_loopback.so
%attr(755,root,root) %{_libdir}/jack/jack_netone.so
%attr(755,root,root) %{_libdir}/jack/jack_net.so
%attr(755,root,root) %{_libdir}/jack/jack_proxy.so
%attr(755,root,root) %{_libdir}/jack/netadapter.so
%attr(755,root,root) %{_libdir}/jack/netmanager.so
%attr(755,root,root) %{_libdir}/jack/profiler.so
%{_datadir}/dbus-1/services/org.jackaudio.service
%{?with_classic:%{_mandir}/man1/jackd.1*}

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjack.so.0
%attr(755,root,root) %{_libdir}/libjacknet.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjacknet.so.0
%attr(755,root,root) %{_libdir}/libjackserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjackserver.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack.so
%attr(755,root,root) %{_libdir}/libjacknet.so
%attr(755,root,root) %{_libdir}/libjackserver.so
%{_includedir}/jack
%{_pkgconfigdir}/jack.pc

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
