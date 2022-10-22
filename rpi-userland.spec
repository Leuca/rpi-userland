Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version lead=0.0 follow=0 }}}
Release:        5%{?dist}
Summary:        Userland tools and libs for the Raspberry Pi

License:        BSD-3
URL:            https://github.com/raspberrypi/userland
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  aarch64

BuildRequires:  git, gcc, gcc-c++, cmake, make, glibc, glibc-devel

Provides:       vcgencmd
Provides:       libfdt.so()(64bit)

Source:         {{{ git_dir_pack }}}

%description
Raspberry Pi ARM side libraries and utilities.
ARM side code to interface to: EGL, mmal, GLESv2, vcos, openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.

%package    examples
Requires:       rpi-userland
Summary:        Userland hello-pi source code

%description    examples
Provides the 'hello-pi' source code from rpi-userland Raspberry Pi ARM side libraries and utilities.

%package    devel
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-static%{?_isa} = %{version}-%{release}
Summary:    Development package for %{name}

%description    devel
Files needed to develop with %{name}

%package    -n libglvnd-devel
Requires:   %{name}%{?_isa} = %{version}-%{release}
Summary:    Fake development package for brcmEGL and brcmGLES
Conflicts:  libglvnd-devel

%description    -n libglvnd-devel
Fake development package for broadcom version of libglvnd libraries for RPi

%prep
{{{ git_dir_setup_macro }}}

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
install -m 0644 build/lib/libfdt.so %{buildroot}%{_libdir}

%files
%license LICENCE
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/plugins/*
%{_mandir}/*
%{_libdir}/plugins/reader_*.so.*
%{_libdir}/plugins/writer_*.so.*

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
%{_libdir}/plugins/reader_*.so
%{_libdir}/plugins/writer_*.so

%files -n libglvnd-devel
%{_includedir}/EGL/*
%{_includedir}/GLES/*
%{_includedir}/GLES2/*
%{_includedir}/KHR/*
%{_libdir}/pkgconfig/brcmegl.pc
%{_libdir}/pkgconfig/brcmglesv2.pc

%changelog
{{{ git_dir_changelog }}}
