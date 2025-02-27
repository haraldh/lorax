# NOTE: This specfile is generated from upstream at https://github.com/rhinstaller/lorax
# NOTE: Please submit changes as a pull request
%define debug_package %{nil}

Name:           lorax
Version:        35.2
Release:        1%{?dist}
Summary:        Tool for creating the anaconda install images

License:        GPLv2+
URL:            https://github.com/weldr/lorax
# To generate Source0 do:
# git clone https://github.com/weldr/lorax
# git checkout -b archive-branch lorax-%%{version}-%%{release}
# tito build --tgz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:       lorax-templates

Requires:       cpio
Requires:       device-mapper
Requires:       dosfstools
Requires:       e2fsprogs
Requires:       findutils
Requires:       gawk
Requires:       xorriso
Requires:       glib2
Requires:       glibc
Requires:       glibc-common
Requires:       gzip
Requires:       isomd5sum
Requires:       module-init-tools
Requires:       parted
Requires:       squashfs-tools >= 4.2
Requires:       util-linux
Requires:       xz-lzma-compat
Requires:       xz
Requires:       pigz
Requires:       pbzip2
Requires:       dracut >= 030
Requires:       kpartx
Requires:       psmisc

# Python modules
Requires:       libselinux-python3
Requires:       python3-mako
Requires:       python3-kickstart >= 3.19
Requires:       python3-dnf >= 3.2.0
Requires:       python3-librepo
Requires:       python3-pycdlib

%if 0%{?fedora}
# Fedora specific deps
%ifarch x86_64
Requires:       hfsplus-tools
%endif
%endif

%ifarch %{ix86} x86_64
Requires:       syslinux >= 6.03-1
Requires:       syslinux-nonlinux >= 6.03-1
%endif

%ifarch ppc64le
Requires:       grub2
Requires:       grub2-tools
%endif

%ifarch s390 s390x
Requires:       openssh
Requires:       s390utils >= 2.15.0-2
%endif

%ifarch %{arm}
Requires:       uboot-tools
%endif

# Moved image-minimizer tool to lorax
Provides:       appliance-tools-minimizer = %{version}-%{release}
Obsoletes:      appliance-tools-minimizer < 007.7-3

%description
Lorax is a tool for creating the anaconda install images.

It also includes livemedia-creator which is used to create bootable livemedia,
including live isos and disk images. It can use libvirtd for the install, or
Anaconda's image install feature.

%package docs
Summary: Lorax html documentation
Requires: lorax = %{version}-%{release}

%description docs
Includes the full html documentation for lorax, livemedia-creator, and the pylorax library.

%package lmc-virt
Summary:  livemedia-creator libvirt dependencies
Requires: lorax = %{version}-%{release}
Requires: qemu

# Fedora edk2 builds currently only support these arches
%ifarch %{ix86} x86_64 %{arm} aarch64
Requires: edk2-ovmf
%endif
Recommends: qemu-kvm

%description lmc-virt
Additional dependencies required by livemedia-creator when using it with qemu.

%package lmc-novirt
Summary:  livemedia-creator no-virt dependencies
Requires: lorax = %{version}-%{release}
Requires: anaconda-core
Requires: anaconda-tui
Requires: anaconda-install-env-deps
Requires: system-logos
Requires: python3-psutil

%description lmc-novirt
Additional dependencies required by livemedia-creator when using it with --no-virt
to run Anaconda.

%package templates-generic
Summary:  Generic build templates for lorax and livemedia-creator
Requires: lorax = %{version}-%{release}
Provides: lorax-templates = %{version}-%{release}

%description templates-generic
Lorax templates for creating the boot.iso and live isos are placed in
/usr/share/lorax/templates.d/99-generic

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

%files
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS
%doc docs/lorax.rst docs/livemedia-creator.rst docs/product-images.rst
%doc docs/*ks
%{python3_sitelib}/pylorax
%{python3_sitelib}/*.egg-info
%{_sbindir}/lorax
%{_sbindir}/mkefiboot
%{_sbindir}/livemedia-creator
%{_sbindir}/mkksiso
%{_bindir}/image-minimizer
%dir %{_sysconfdir}/lorax
%config(noreplace) %{_sysconfdir}/lorax/lorax.conf
%dir %{_datadir}/lorax
%{_mandir}/man1/lorax.1*
%{_mandir}/man1/livemedia-creator.1*
%{_mandir}/man1/mkksiso.1*
%{_tmpfilesdir}/lorax.conf

%files docs
%doc docs/html/*

%files lmc-virt

%files lmc-novirt

%files templates-generic
%dir %{_datadir}/lorax/templates.d
%{_datadir}/lorax/templates.d/*

%changelog
* Wed May 05 2021 Brian C. Lane <bcl@redhat.com> 35.2-1
- runtime-cleanup: Use branding package name instead of product.name (bcl@redhat.com)
- treebuilder: Add branding package to template variables (bcl@redhat.com)
- livemedia-creator: Use inst.ks on cmdline for virt (bcl@redhat.com)
- docs: Remove composer-cli.1 (bcl@redhat.com)

* Mon Apr 26 2021 Brian C. Lane <bcl@redhat.com> 35.1-1
- New lorax documentation - 35.1 (bcl@redhat.com)
- Makefile: Use podman as a user for testing and docs (bcl@redhat.com)
- composer-cli: Remove all traces of composer-cli (bcl@redhat.com)
- livemedia-creator: Add rhgb to live iso cmdline (#1943312) (bcl@redhat.com)
- tests: Fix pocketlint use of removed pylint messages (bcl@redhat.com)
- Disable X11 forwarding from installation environment. (vslavik@redhat.com)
- Remove display-related packages (vslavik@redhat.com)
- Drop trying to install reiserfs-utils (kevin@scrye.com)
- test: Fix URL to bots testmap (martin@piware.de)
- Change khmeros-base-fonts to khmer-os-system-fonts. (pnemade@fedoraproject.org)
- Fix output path in docs (vslavik@redhat.com)
- runtime-cleanup: don't wipe /usr/bin/report-cli (#1937550) (awilliam@redhat.com)
- xorg-x11-font-utils is now four packages, remove all of them (peter.hutterer@who-t.net)
- xorg-x11-server-utils was split up in Fedora 34, so adjust templates (kevin@scrye.com)
* Wed Mar 03 2021 Brian C. Lane <bcl@redhat.com> 35.0-1
- New lorax documentation - 35.0 (bcl@redhat.com)
- Makefile: Add test-in-podman and docs-in-podman build targets (bcl@redhat.com)
- isolinux.cfg: Rename the 'vesa' menu entry to 'basic' (bcl@redhat.com)
- composer-cli: Add support for start-ostree --url URL (bcl@redhat.com)

* Wed Mar 03 2021 Brian C. Lane <bcl@redhat.com>
- New lorax documentation - 35.0 (bcl@redhat.com)
- Makefile: Add test-in-podman and docs-in-podman build targets (bcl@redhat.com)
- isolinux.cfg: Rename the 'vesa' menu entry to 'basic' (bcl@redhat.com)
- composer-cli: Add support for start-ostree --url URL (bcl@redhat.com)

* Mon Feb 15 2021 Brian C. Lane <bcl@redhat.com> 34.9-1
- Use inst.rescue to trigger rescue mode (awilliam@redhat.com)
  Resolves: rhbz#1928318
* Mon Feb 08 2021 Brian C. Lane <bcl@redhat.com> 34.8-1
- Use image dependencies metapackage (vslavik@redhat.com)
- tests: Include the fedora-updates repo when testing boot.iso building (bcl@redhat.com)

* Wed Jan 20 2021 Brian C. Lane <bcl@redhat.com> 34.7-1
- live/x86.tmpl: Copy livecd-iso-to-disk script, if installed (david.ward@ll.mit.edu)
- templates: Copy license files from the correct path (david.ward@ll.mit.edu)
- test: Fix vm.install for non-LVM cloud images (martin@piware.de)

* Wed Dec 16 2020 Brian C. Lane <bcl@redhat.com> 34.6-1
- Remove LD_PRELOAD libgomp.so.1 from lmc --no-virt (bcl@redhat.com)
- Add POSTIN scriptlet error to the log monitor list (bcl@redhat.com)
- Improve lmc no-virt error handling (bcl@redhat.com)
- lorax.spec: Drop GConf2 requirement (bcl@redhat.com)

* Mon Nov 30 2020 Brian C. Lane <bcl@redhat.com> 34.5-1
- Don't remove libldap_r libraries during runtime-cleanup.tmpl (spichugi@redhat.com)
- Do not use '--loglevel' option when running Anaconda (vtrefny@redhat.com)
- Makefile: quiet rsync use in testing (bcl@redhat.com)
- Switch to using GitHub Actions instead of Travis CI (bcl@redhat.com)

* Mon Nov 02 2020 Brian C. Lane <bcl@redhat.com> 34.4-1
- Update the default release version to 34 (bcl@redhat.com)
- Remove mdmonitor service from boot.iso (bcl@redhat.com)
- Switch to using upstream mk-s390image for s390 cdboot.img creation (bcl@redhat.com)
- sshd_config: Apply suggested changes (bcl@redhat.com)
- lorax.spec: Add BuildRequires on systemd-rpm-macros for tmpfilesdir macro (bcl@redhat.com)

* Wed Oct 07 2020 Brian C. Lane <bcl@redhat.com> 34.3-1
- composer: Fix open file warnings (bcl@redhat.com)
- ltmpl: Fix deprecated escape in docstring (bcl@redhat.com)
- tests: Fix open file warning in test_execWithRedirect (bcl@redhat.com)
- Cleanup imgutil open files and processes (bcl@redhat.com)
- tests: Remove test_del_execReadlines (bcl@redhat.com)
- Fix unclosed files (bcl@redhat.com)
- test: Use Python dev mode during testing (bcl@redhat.com)
- tests: Update composer-cli blueprint server tests (bcl@redhat.com)
- runtime-cleanup: Delete .pyc files (bcl@redhat.com)
- New lorax documentation - 34.3 (bcl@redhat.com)
- doc: Add Blueprint documentation and example to composer-cli.rst (bcl@redhat.com)
- docs: Update docs for lorax-composer removal (bcl@redhat.com)
- tests: Remove unused lorax-composer tests (bcl@redhat.com)
- Remove lorax-composer, it has been replaced by osbuild-composer (bcl@redhat.com)

* Tue Sep 29 2020 Brian C. Lane <bcl@redhat.com> 34.2-1
- runtime-cleanup: Remove ncurses package (bcl@redhat.com)

* Mon Sep 14 2020 Brian C. Lane <bcl@redhat.com> 34.1-1
- Fix broken single-item tuples in a few places (awilliam@redhat.com)
- Drop dpaa2 firmware on non-aarch64 arches (awilliam@redhat.com)
- Drop firmware for Mellanox Spectrum (awilliam@redhat.com)
- runtime-cleanup: big refresh of stale things (awilliam@redhat.com)

* Tue Sep 08 2020 Brian C. Lane <bcl@redhat.com> 34.0-1
- New lorax documentation - 34.0 (bcl@redhat.com)
- runtime-cleanup: strip a bunch of unnecessary firmwares (awilliam@redhat.com)
- runtime-install: specify polkit-gnome to avoid lxpolkit and GTK2 (awilliam@redhat.com)
- runtime-install: exclude gnome-firmware and sigrok-firmware (awilliam@redhat.com)
- runtime-cleanup: Drop video playback acceleration drivers (awilliam@redhat.com)
- runtime-install: don't install notification-daemon (awilliam@redhat.com)
