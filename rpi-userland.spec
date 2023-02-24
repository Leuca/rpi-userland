Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=0.0 follow=0 }}}
Release:        6%{?dist}
Summary:        Userland tools and libs for the Raspberry Pi

License:        BSD-3
URL:            https://github.com/raspberrypi/userland
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  aarch64

BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  libfdt-devel

Provides:       vcgencmd

Source:         {{{ git_dir_pack }}}

Patch0:         rpi-userland-add-soversion.patch
Patch1:         rpi-userland-libfdt-fix.patch

%description
Raspberry Pi ARM side libraries and utilities.
ARM side code to interface to: mmal, vcos, vchiq_arm, bcm_host.

%package    examples
Requires:       %{name}
Summary:        Userland hello-pi source code

%description    examples
Provides the 'hello-pi' source code from rpi-userland Raspberry Pi ARM side libraries and utilities.

%package    devel
Requires:   %{name}%{?_isa} = %{version}-%{release}
Summary:    Development package for %{name}

%description    devel
Files needed to develop with %{name}


%prep
{{{ git_dir_setup_macro }}}
%autopatch -p1

%build
%cmake \
        -DARM64:BOOL=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_SHARED_LIBS:BOOL=ON \
        -DBUILD_STATIC_LIBS:BOOL=OFF \
        -DVMCS_INSTALL_PREFIX=%{_prefix} \

%cmake_build

%install
%cmake_install
%ifarch aarch64
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
%endif
mkdir -p %{buildroot}%{_datadir}
mv %{buildroot}%{_prefix}/man %{buildroot}%{_datadir}

%files
%license LICENCE
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/*

%files examples
%{_usrsrc}/*

%files devel
%{_includedir}/IL/*
%{_includedir}/VG/*
%{_includedir}/WF/*
%{_includedir}/bcm_host.h
%{_includedir}/interface/*
%{_includedir}/vcinclude/*
%{_libdir}/pkgconfig/bcm_host.pc
%{_libdir}/pkgconfig/brcmvg.pc
%{_libdir}/pkgconfig/mmal.pc
%{_libdir}/pkgconfig/vcsm.pc
%{_libdir}/*.so
%ghost %{_includedir}/EGL/*
%ghost %{_includedir}/GLES/*
%ghost %{_includedir}/GLES2/*
%ghost %{_includedir}/KHR/*
%ghost %{_libdir}/pkgconfig/brcmegl.pc
%ghost %{_libdir}/pkgconfig/brcmglesv2.pc


%changelog
{{{ git_dir_changelog }}}
