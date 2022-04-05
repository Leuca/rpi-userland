Name:           {{{ git_dir_name }}}
Version:        {{{ git_dir_version }}}
Release:        2%{?dist}
Summary:        Userland tools and libs for the Raspberry Pi

License:        BSD-3
URL:            https://github.com/raspberrypi/userland
VCS:            {{{ git_dir_vcs }}}

ExclusiveArch:  %{arm} aarch64

BuildRequires:  git, gcc, gcc-c++, cmake, make, glibc, glibc-devel

Provides:       vcgencmd

Source:         {{{ git_dir_pack }}}

%package examples
Requires:       rpi-userland
Summary:        Userland hello-pi source code

%description
Raspberry Pi ARM side libraries and utilities.
ARM side code to interface to: EGL, mmal, GLESv2, vcos, openmaxil, vchiq_arm, bcm_host, WFC, OpenVG.

%description examples
Provides the 'hello-pi' source code from rpi-userland Raspberry Pi ARM side libraries and utilities.

%prep
%setup -T -b 0 -q -n rpi-userland


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
%{_includedir}/*
%{_libdir}/*
%{_bindir}/*
%{_mandir}/*

%files examples
%{_usrsrc}/*

%changelog
