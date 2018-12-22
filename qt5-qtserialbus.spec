%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta %{nil}

%define qtserialbus %mklibname qt%{api}serialbus %{major}
%define qtserialbusd %mklibname qt%{api}serialbus -d
%define qtserialbus_p_d %mklibname qt%{api}serialbus-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtserialbus
Version:	5.12.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtserialbus-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%(echo %{beta} |sed -e "s,1$,,")/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtserialbus-everywhere-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
Summary:	Qt library for accessing industrial serial buses
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
BuildRequires:	qmake5 >= %{version}
BuildRequires:	pkgconfig(Qt5Core) >= %{version}
BuildRequires:	pkgconfig(Qt5Widgets) >= %{version}
BuildRequires:	pkgconfig(Qt5Network) >= %{version}
BuildRequires:	pkgconfig(Qt5SerialPort) >= %{version}
BuildRequires:	pkgconfig(Qt5Test) >= %{version}
BuildRequires:	pkgconfig(libudev)
# For the Provides: generator
BuildRequires:	cmake >= 3.11.0-1

%description
Qt library for accessing various industrial serial buses
and protocols, such as CAN, ModBus

%files
%{_libdir}/qt5/bin/canbusutil
%{_libdir}/qt5/plugins/canbus

#------------------------------------------------------------------------------

%package -n %{qtserialbus}
Summary: Qt%{api} Component Library
Group: System/Libraries

%description -n %{qtserialbus}
Qt%{api} Component Library.

Qt library for accessing various industrial serial buses
and protocols, such as CAN, ModBus

%files -n %{qtserialbus}
%{_qt5_libdir}/libQt5SerialBus.so.%{api}*

#------------------------------------------------------------------------------

%package -n %{qtserialbusd}
Summary: Devel files needed to build apps based on QtSerialbus
Group: Development/KDE and Qt
Requires: %{qtserialbus} = %version

%description -n %{qtserialbusd}
Devel files needed to build apps based on Qt Serialbus.

Qt library for accessing various industrial serial buses
and protocols, such as CAN, ModBus

%files -n %{qtserialbusd}
%{_qt5_libdir}/libQt5SerialBus.prl
%{_qt5_libdir}/libQt5SerialBus.so
%{_qt5_libdir}/pkgconfig/Qt5SerialBus.pc
%{_qt5_libdir}/cmake/Qt5SerialBus
%{_qt5_prefix}/mkspecs/modules/qt_lib_serialbus.pri
%{_qt5_includedir}/QtSerialBus
%exclude %{_qt5_includedir}/QtSerialBus/%version

#------------------------------------------------------------------------------

%package -n %{qtserialbus_p_d}
Summary: Devel files needed to build apps based on QtSerialbus
Group:    Development/KDE and Qt
Requires: %{qtserialbusd} = %version
Provides: qt5-serialbus-private-devel = %version

%description -n %{qtserialbus_p_d}
Devel files needed to build apps based on QtSerialbus.

%files -n %{qtserialbus_p_d}
%{_qt5_includedir}/QtSerialBus/%version
%{_qt5_prefix}/mkspecs/modules/qt_lib_serialbus_private.pri

#------------------------------------------------------------------------------

%package examples
Summary: Examples for the Qt SerialBus library
Group: Development/KDE and Qt

%description examples
Examples for the Qt SerialBus library

%files examples
%{_qt5_prefix}/examples/*

#------------------------------------------------------------------------------

%prep
%autosetup -n %qttarballdir -p1

%build
%qmake_qt5
%make_build

#------------------------------------------------------------------------------
%install
%make_install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
