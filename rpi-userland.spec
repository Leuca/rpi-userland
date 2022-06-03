Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version }}}
Release:        4%{?dist}
Summary:        Userland tools and libs for the Raspberry Pi

License:        BSD-3
URL:            https://github.com/raspberrypi/userland
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  %{arm} aarch64

BuildRequires:  git, gcc, gcc-c++, cmake, make, glibc, glibc-devel

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Provides:       vcgencmd

Source:         {{{ git_dir_pack }}}

%description
Raspberry Pi ARM side libraries and utilities.
ARM side code to interface to: EGL, mmal, GLESv2, vcos, openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.

%package	examples
Requires:       rpi-userland
Summary:        Userland hello-pi source code

%description	examples
Provides the 'hello-pi' source code from rpi-userland Raspberry Pi ARM side libraries and utilities.

%package	libs
Requires:	%{name}%{?_isa} = %{version}-%{release}
Summary:	%{name} libraries
Provides:	libglvnd libglvnd-egl libglvnd-gles

%description	libs
Raspberry Pi ARM side libraries

%package	libs-devel
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Summary:	Development package for %{name}
Provides:	libglvnd-devel

%description	libs-devel
Files needed to develop with %{name}

%prep
{{{ git_dir_setup_macro }}}

%build
mkdir -p build/rpm/release
pushd build/rpm/release
%ifarch %{arm}
cmake -DCMAKE_BUILD_TYPE=Release -DARM64=OFF ../../..
%endif
%ifarch aarch64
cmake -DCMAKE_BUILD_TYPE=Release -DARM64=ON ../../..
%endif
make -j `nproc`



%install
mkdir -p %{buildroot}/%{_prefix}
pushd build/rpm/release
make install DESTDIR=%{buildroot}
mv %{buildroot}/opt/vc/* %{buildroot}/%{_prefix}
rm -rf %{buildroot}/opt
%ifarch aarch64
mv %{buildroot}/%{_prefix}/lib %{buildroot}/%{_libdir}
%endif
mkdir -p %{buildroot}/%{_mandir}
mv %{buildroot}/%{_prefix}/man %{buildroot}/%{_datadir}



%files
%license LICENCE
%{_bindir}/*
%{_mandir}/*

%files examples
%{_usrsrc}/*

%files libs
%{_libdir}/lib*

%files libs-devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%changelog
{{{ git_dir_changelog }}}
