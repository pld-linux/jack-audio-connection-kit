#
# Conditional build:
%bcond_with	cap		# use capabilities to get real-time priority (needs suid root binary)
%bcond_without	alsa		# don't build ALSA driver
%bcond_without	static_libs	# don't build static libs
#
Summary:	The JACK Audio Connection Kit
Summary(pl):	JACK - zestaw do po³±czeñ audio
Name:		jack-audio-connection-kit
Version:	0.99.0
Release:	1
License:	LGPL (libjack), GPL (the rest)
Group:		Daemons
Source0:	http://dl.sourceforge.net/jackit/%{name}-%{version}.tar.gz
# Source0-md5:	a891a699010452258d77e59842ebe4a0
URL:		http://jackit.sourceforge.net/
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 0.9.0}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
%{?with_cap:BuildRequires:	libcap-devel}
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
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

%package devel
Summary:	Header files for JACK
Summary(pl):	JACK - pliki nag³ówkowe
License:	LGPL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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

%package driver-alsa
Summary:	ALSA driver for JACK
Summary(pl):	Sterownik ALSA dla JACKa
License:	GPL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description driver-alsa
ALSA driver for JACK.

%description driver-alsa -l pl
Sterownik ALSA dla JACKa.

%package example-clients
Summary:	Example clients that use JACK
Summary(pl):	Przyk³adowe programy kliencie u¿ywaj±ce JACKa
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

%build
cp -f /usr/share/automake/config.sub config
%{__autoconf}
# --enable-optimize is heavy broken, it uses information from /proc/cpuinfo to set compilator flags
%configure \
	%{!?with_alsa:--disable-alsa} \
	%{?with_cap:--enable-capabilities %{!?debug:--enable-stripped-jackd}} \
	%{?debug:--enable-debug} \
	--disable-optimize \
	--enable-posix-shm \
	%{?with_static_libs:--enable-static} \
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# note: COPYING only specifies which parts fall under GPL and LGPL
%doc AUTHORS TODO COPYING
%{?_with_cap:%attr(4755,root,root) %{_bindir}/jackstart}
%attr(755,root,root) %{_bindir}/jackd
%attr(755,root,root) %{_bindir}/jack_load
%attr(755,root,root) %{_bindir}/jack_unload
%attr(755,root,root) %{_libdir}/libjack.so.*.*
%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_oss.so
%{_mandir}/man1/*

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

%if %{with alsa}
%files driver-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
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
