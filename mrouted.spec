Summary:	Multicast routing daemon
Summary(pl.UTF-8):	Demon routingu multicastowego
Name:		mrouted
Version:	3.9beta3+IOS12
Release:	0
License:	custom
Group:		Networking/Daemons
Source0:	ftp://ftp.research.att.com/dist/fenner/mrouted/%{name}-%{version}.tar.gz
# Source0-md5:	15bb287b5af0cef4ec8e4ad3bd56740c
Source1:	%{name}.init
Patch0:		%{name}-linux-glibc.patch
Patch1:		%{name}-pointtopoint.patch
Patch2:		%{name}-paths.patch
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	yacc
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mrouted is an implementation of the Distance-Vector Multicast Routing
Protocol (DVMRP), an earlier version of which is specified in
RFC-1075. It maintains topological knowledge via a distance-vector
routing protocol (like RIP, described in RFC-1058), upon which it
implements a multicast datagram forwarding algorithm called Reverse
Path Multicasting.

%description -l pl.UTF-8
mrouted to implementacja DVMRP (Distance-Vector Multicast Routing
Protocol), którego wcześniejsza wersja jest opisana w RFC-1075. Zbiera
informacje topologiczne przez protokół discance-vector routing
(podobny do RIP, opisany w RFC-1058), a na ich podstawie implementuje
algorytm forwardowania datagramów multicastowych nazywany Reverse Path
Multicasting.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} \
	CFLAGS="%{rpmcflags} -DRAW_INPUT_IS_RAW -DRAW_OUTPUT_IS_RAW -DIOCTL_OK_ON_RAW_SOCKET"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir},%{_mandir}/man8}
install map-mbone mrinfo mrouted $RPM_BUILD_ROOT%{_sbindir}
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8
install mrouted.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mrouted

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mrouted
%service mrouted restart "routing daemon"

%preun
if [ "$1" = "0" ]; then
	%service mrouted stop
	/sbin/chkconfig --del mrouted
fi

%files
%defattr(644,root,root,755)
%doc README* LICENSE
%{_mandir}/man8/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mrouted.conf
