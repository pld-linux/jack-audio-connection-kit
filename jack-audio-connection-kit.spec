#
# Conditional build:
%bcond_with cap			# use capabilities to get real-time priority (needs suid root binary)
%bcond_without static_libs	# build static libs
#
Summary:	The Jack Audio Connection Kit
Summary(pl):	Jack - zestaw do po³±czeñ audio
Name:		jack-audio-connection-kit
Version:	0.92.0
Release:	1
License:	GPL/LGPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/jackit/%{name}-%{version}.tar.gz
# Source0-md5:	b98a2f9db7833df1c7a01f80ff9090d1
Patch0:		%{name}-opt.patch
URL:		http://jackit.sourceforge.net/
BuildRequires:	alsa-lib-devel >= 0.9.0
BuildRequires:	autoconf
BuildRequires:	doxygen
BuildRequires:	glib-devel >= 1.0.0
%{?with_cap:BuildRequires:	libcap-devel}
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	readline-devel
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
Summary:	Header files for Jack
Summary(pl):	Jack - pliki nag³ówkowe
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for the Jack Audio Connection Kit.

%description devel -l pl
Pliki nag³ówkowe dla zestawu do po³±czeñ audio Jack.

%package static
Summary:	Static Jack library
Summary(pl):	Statyczna biblioteka Jack
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static Jack library.

%description static -l pl
Statyczna biblioteka Jack.

%package example-clients
Summary:	Example clients that use Jack
Summary(pl):	Przyk³adowe programy kliencie u¿ywaj±ce Jacka
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description example-clients
Small example clients that use the Jack Audio Connection Kit.

%description example-clients -l pl
Ma³e, przyk³adowe programy klienckie, które u¿ywaj± zestawu do
po³±czeñ audio Jack.

%package example-jackrec
Summary:	Example Jack client: jackrec
Summary(pl):	Przyk³adowy klient zestawu Jack: jackrec
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description example-jackrec
Example Jack client: jackrec. It's separated because it uses
libsndfile library.

%description example-jackrec
Przyk³adowy klient zestawu Jack: jackrec. Jest wydzielony, poniewa¿
wymaga biblioteki libsndfile.

%prep
%setup -q
%patch -p1

%build
%{__autoconf}
CPPFLAGS="-I/usr/X11R6/include"
%configure \
	%{?with_cap:--enable-capabilities %{!?debug:--enable-stripped-jackd}} \
	%{?debug:--enable-debug} \
	%{!?debug:--enable-optimize} \
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
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
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
