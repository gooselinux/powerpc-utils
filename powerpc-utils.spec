Name:           powerpc-utils
Version:        1.2.2
Release:        17%{?dist}
Summary:        Utilities for PowerPC platforms

Group:          System Environment/Base
License:        CPL
URL:            http://sourceforge.net/projects/%{name}/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        nvsetenv
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  doxygen automake librtas-devel libservicelog-devel >= 1.0.1-2

# should be fixed - libservicelog is not right name
Requires:       libservicelog 
ExclusiveArch:  ppc ppc64

# This hack is needed only for platforms with autoconf < 2.63
Patch1:		powerpc-utils-autoconf.patch

# allow setting run-mode value. bz 418836
Patch2:		powerpc-utils-cpu_diag_mode.patch

# 599711
Patch3:		powerpc-utils-lsdevinfo.patch

# 599711, new ls-{vscsi,vdev,veth} scripts
Patch4:		powerpc-utils-lsvio.patch

# 599714, correct searching in sysfs
Patch5:		powerpc-utils-multieth.patch

# 599714, Update ofpathname to use udevadm
Patch6:		powerpc-utils-udevadm.patch

# Fix some warnings. Pre-req for patch8,9
Patch7:		powerpc-utils-warnings.patch

# pre-req for Patch9.
Patch8:		powerpc-utils-threads.patch

# 599716, Use hex values
Patch9:		powerpc-utils-cpudscr.patch

# 599719, Correct cpu dlpar capable check
Patch10:	powerpc-utils-cpu_dlpar_check.patch

# Corrects the parameter handling of ppc64_cpu when setting the run-mode
Patch11:	powerpc-utils-run_mode.patch

# 602717, amsstat changes from upstream
Patch12:	powerpc-utils-amsstat.patch

# 607356, ofpathname man page update
Patch13:	powerpc-utils-man_ofpathname.patch

# 619210, CPU  DLPAR can be done completely in the kernel
Patch14:	powerpc-utils-cpu_dlpar_kernel.patch

# 620796, sysfs memory layout changed, make memory hotplug work again
Patch15:	powerpc-utils-drmgr_memory.patch

# 624171, Allow DLPAR to remove Ethernet controller on power 7
Patch16:	powerpc-utils-dlpar_ethernet.patch

# This is done before release of F12
Obsoletes:      powerpc-utils-papr < 1.1.6-3
Provides:       powerpc-utils-papr = 1.1.6-3

%description
Utilities for PowerPC platforms.

%prep
%setup -q

# This hack is needed only for platforms with autoconf < 2.63
%if 0%{?fedora} < 9 && 0%{?rhel} < 6
%patch1 -p1 -b .aconf
%endif

%patch2 -p1 -b .cpu_diag_mode
%patch3 -p1 -b .lsdevinfo
%patch4 -p1 -b .lsvio
%patch5 -p1 -b .multieth
%patch6 -p1 -b .udevadm
%patch7 -p1 -b .warnings
%patch8 -p1 -b .threads
%patch9 -p1 -b .cpudscr
%patch10 -p1 -b .cpu_dlpar_check
%patch11 -p1 -b .run_mode
%patch12 -p1 -b .amsstat
%patch13 -p1 -b .man_ofpathname
%patch14 -p1 -b .cpu_dlpar_kernel
%patch15 -p1 -b .drmgr_memory
%patch16 -p1 -b .dlpar_ehternet

%build
./bootstrap.sh
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT FILES= RCSCRIPTS=
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/nvsetenv

%define pkgdocdir %{_datadir}/doc/%{name}-%{version}
# move doc files
mkdir -p $RPM_BUILD_ROOT%{pkgdocdir}
install $RPM_BUILD_ROOT/usr/share/doc/packages/powerpc-utils/* -t $RPM_BUILD_ROOT%{pkgdocdir}
rm -rf $RPM_BUILD_ROOT/usr/share/doc/packages/powerpc-utils

# init script and perl script are deprecated. Removing them
rm -rf $RPM_BUILD_ROOT/etc/init.d/ibmvscsis.sh $RPM_BUILD_ROOT/usr/sbin/vscsisadmin

# nvsetenv is just a wrapper to nvram
ln -s nvram.8.gz $RPM_BUILD_ROOT/%{_mandir}/man8/nvsetenv.8.gz

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_sbindir}/nvsetenv
%{_sbindir}/nvram
%{_sbindir}/snap
%{_sbindir}/bootlist
%{_sbindir}/ofpathname
%{_sbindir}/ppc64_cpu
%{_sbindir}/lsdevinfo
%{_sbindir}/lsprop
%{_mandir}/man8/nvram.8*
%{_mandir}/man8/nvsetenv.8*
%{_mandir}/man8/snap.8*
%{_mandir}/man8/bootlist.8*
%{_mandir}/man8/ofpathname.8*

%{_sbindir}/update_flash
%{_sbindir}/activate_firmware
%{_sbindir}/usysident
%{_sbindir}/usysattn
%{_sbindir}/set_poweron_time
%{_sbindir}/rtas_ibm_get_vpd
%{_sbindir}/serv_config
%{_sbindir}/uesensor
%{_sbindir}/hvcsadmin
%{_sbindir}/rtas_dump
%{_sbindir}/rtas_event_decode
%{_sbindir}/sys_ident
%{_sbindir}/drmgr
%{_sbindir}/lsslot
%{_sbindir}/ls-vdev
%{_sbindir}/ls-veth
%{_sbindir}/ls-vscsi

%{_bindir}/amsstat
%{_mandir}/man8/update_flash.8*
%{_mandir}/man8/activate_firmware.8*
%{_mandir}/man8/usysident.8*
%{_mandir}/man8/usysattn.8*
%{_mandir}/man8/set_poweron_time.8*
%{_mandir}/man8/rtas_ibm_get_vpd.8*
%{_mandir}/man8/serv_config.8*
%{_mandir}/man8/uesensor.8*
%{_mandir}/man8/hvcsadmin.8*
%{_mandir}/man8/vscsisadmin.8*
%{_mandir}/man8/ibmvscsis.sh.8*
%{_mandir}/man8/ibmvscsis.conf.8*
%{_mandir}/man8/rtas_dump.8*
%{_mandir}/man8/sys_ident.8*
%{_mandir}/man1/amsvis.1*
%{_mandir}/man1/amsstat.1*
%doc README COPYRIGHT Changelog

%post

%preun

%changelog
* Wed Aug 18 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-17
- Allow DLPAR to remove ethernet controller on power 7
  Resolves: #624171

* Thu Aug 05 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-16
- Make memory hotplug work again
  Resolves: #620796

* Fri Jul 30 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-15
- CPU  DLPAR can be done completely in the kernel
  Resolves: #619210

* Thu Jun 24 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-14
- Compile with -fno-strict-aliasing CFLAG
- linked nvsetenv man page to nvram man page
  Resolves: #596196

* Thu Jun 24 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-13
- Updated man page of ofpathname
  Resolves: #607356

* Tue Jun 22 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-12
- Updated amsstat script
  Resolves: #602717

* Tue Jun 15 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-11
- Correct the parameter handling of ppc64_cpu when setting the run-mode
  Resolves: #603134

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-10
- Correct cpu dlpar capable check
  Resolves: #599719

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-9
- Added missing prerequired patches
  Resolves: #599716

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-8
- New common read/write routines in ppc64_cpu
  Resolves: #599716

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-7
- Correct the searching in sysfs for an ethernet devices' open
firmware device path name.
- Update ofpathname to use udevadm
  Resolves: #599714

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-6
- Added missing scripts to files section
  Resolves: #599711

* Wed Jun 09 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-5
- lsdevinfo fixes for Power 6 machine with Virtual Fibre Channel
  Resolves: #599711

* Wed Jun 02 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-4
- Allow setting run mode
  Resolves: #598714

* Fri Mar 05 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-3
- Do not manage init script. It is no more here.

* Fri Mar 05 2010 Roman Rakus <rrakus@redhat.com> - 1.2.2-2
- Removed deprecated init script and perl script

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.2-1.1
- Rebuilt for RHEL 6

* Thu Oct 29 2009 Stepan Kasal <skasal@redhat.com> - 1.2.2-1
- new upstream version
- amsvis removed, this package has no longer anything with python
- change the manual pages in the file list so that it does not depend on
  particular compression used
- add patch for configure.ac on platforms with autoconf < 2.63
- use standard %%configure/make in %%build

* Mon Aug 17 2009 Roman Rakus <rrakus@redhat.com> - 1.2.0-1
- Bump tu version 1.2.0 - powerpc-utils and powerpc-utils-papr get merged

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 06 2009 Roman Rakus <rrakus@redhat.com> - 1.1.3-1
- new upstream version 1.1.3

* Tue Mar 03 2009 Roman Rakus <rrakus@redhat.com> - 1.1.2-1
- new upstream version 1.1.2

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Roman Rakus <rrakus@redhat.com> - 1.1.1-1
- new upstream version 1.1.1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.6-3
- Autorebuild for GCC 4.3

* Mon Dec  3 2007 David Woodhouse <dwmw2@redhat.com> 1.0.6-2
- Add --version to nvsetenv, for ybin compatibility

* Fri Nov 23 2007 David Woodhouse <dwmw2@redhat.com> 1.0.6-1
- New package, split from ppc64-utils
