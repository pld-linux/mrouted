Summary:	Multicast routing daemon
Summary(pl):	Demon routingu multicastowego
Name:		mrouted
Version:	3.9beta3+IOS12
Release:	0
License:	Custom
Group:		Networking/Daemons
Source0:	ftp://ftp.research.att.com/dist/fenner/mrouted/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-linux-glibc.patch
Patch1:		%{name}-pointtopoint.patch
Patch2:		%{name}-paths.patch
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
BuildRequires:	yacc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mrouted is an implementation of the Distance-Vector Multicast Routing
Protocol (DVMRP), an earlier version of which is specified in
RFC-1075. It maintains topological knowledge via a distance-vector
routing protocol (like RIP, described in RFC-1058), upon which it
implements a multicast datagram forwarding algorithm called Reverse
Path Multicasting.

%description -l pl
mrouted to implementacja DVMRP (Distance-Vector Multicast Routing
Protocol), którego wsze¶niejsza wersja jest opisana w RFC-1075. Zbiera
informacje topologiczne przez protokó³ discance-vector routing
(podobny do RIP, opisany w RFC-1058), a na ich podstawie implementuje
algorytm forwardowania datagramów multicastowych nazywany Reverse Path
Multicasting.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} CFLAGS="%{rpmcflags} -DRAW_INPUT_IS_RAW -DRAW_OUTPUT_IS_RAW -DIOCTL_OK_ON_RAW_SOCKET"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_sbindir},%{_mandir}/man8}
install map-mbone mrinfo mrouted $RPM_BUILD_ROOT%{_sbindir}
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8
install mrouted.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/mrouted

gzip -9nf README* LICENSE

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mrouted
if [ -f /var/lock/subsys/mrouted ]; then
	/etc/rc.d/init.d/mrouted restart >&2
else
	echo "Run '/etc/rc.d/init.d/mrouted start' to start routing deamon." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mrouted ]; then
		/etc/rc.d/init.d/mrouted stop >&2
	fi
        /sbin/chkconfig --del mrouted >&2
fi

%files
%defattr(644,root,root,755)
%doc README*.gz LICENSE.gz
%{_mandir}/man8/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mrouted.conf
