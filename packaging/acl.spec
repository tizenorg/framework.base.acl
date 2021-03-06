Name:           acl
Version:        2.2.49
Release:        1
License:        GPLv2
Summary:        Access control list utilities
Url:            http://savannah.nongnu.org/projects/acl
Group:          System/Base
Source:         http://download.savannah.gnu.org/releases/acl/acl-%{version}.src.tar.gz

# SLP patches
Patch0: 01-Makefile.patch
Patch1: 03-re-stat_file_after_chown.patch
Patch2: 04-print_useful_error_from_read_acl_comments.patch
Patch3: 05-restore_crash_on_malformed_input.patch
Patch4: 06-fix_potential_null_pointer_dereference.patch
Patch5: 02-499076-physical-walk.patch
Patch6: 09-prevent_setfacl_--restore_from_SIGSEGV.patch

BuildRequires:  libattr-devel >= 2.4.1
BuildRequires:  gettext-tools

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
License:        LGPLv2.1
Summary:        Dynamic library for access control list support
Group:          System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
License:        LGPL
Summary:        Access control list static libraries and headers
Group:          Development/Libraries
Requires:       libacl = %{version}
Requires:       libattr-devel

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 
%patch4 -p1 
%patch5 -p1 
%patch6 -p1 

%build
export INSTALL_USER=root INSTALL_GROUP=root
make configure
make default
cd po; rm -rf acl.pot; make acl.pot

%install
DIST_ROOT=%{buildroot} make -C . install
DIST_ROOT=%{buildroot} make -C . install-dev
DIST_ROOT=%{buildroot} make -C . install-lib
DIST_ROOT=%{buildroot} make -C build src-manifest

rm -f %{buildroot}/lib/*.a
rm -f %{buildroot}/lib/*.la
rm -rf %{buildroot}%{_defaultdocdir}

# fix links to shared libs and permissions
rm -f %{buildroot}/%{_libdir}/libacl.so
ln -sf ../../%{_lib}/libacl.so %{buildroot}/%{_libdir}/libacl.so
chmod 0755 %{buildroot}/%{_lib}/libacl.so.*.*.*

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig


%docs_package

%files
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_prefix}/share/locale/*/LC_MESSAGES/*.mo

%files -n libacl-devel
/%{_lib}/libacl.so
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_libdir}/libacl.*

%files -n libacl
/%{_lib}/libacl.so.*
