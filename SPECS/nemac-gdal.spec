Name:           nemac-gdal
Version:        1.11.1
Release:        1%{?dist}
Summary:        NEMAC's custom build of GDAL

Group:          Applications/Engineering
License:        GPLV2+
URL:            http://www.gdal.org
Source0:        gdal-%{version}.tar.gz

BuildRequires:  netcdf-devel

Requires:       netcdf

%description
This is NEMAC's custom build of GDAL for use on servers.

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n gdal-%{version}

%build
%configure --with-netcdf --datadir="%{_datadir}/gdal"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root, 0755)
%{_bindir}/*
#%{_datadir}/gdal/
%{_datadir}/
%{_libdir}/libgdal.so.*



%files devel
%defattr(-, root, root, 0755)
%{_includedir}/*.h
%exclude %{_libdir}/libgdal.so.*
%exclude %{_libdir}/*.la
%{_libdir}


%changelog
