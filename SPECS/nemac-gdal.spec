%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:           nemac-gdal
Version:        1.11.1
Release:        4%{?dist}
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

%package python
Summary: Python support for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: python

%description python
This package provides Python bindings for %{name}.

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^%{python_sitearch}/.*\.so$

%prep
%setup -q -n gdal-%{version}

# Fix Python installation path
sed -i 's|setup.py install|setup.py install --root=%{buildroot}|' swig/python/GNUmakefile

%build
%configure --with-netcdf --with-python --datadir="%{_datadir}/gdal"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_datadir}/gdal/
%{_libdir}/libgdal.so.*



%files devel
%defattr(-, root, root, 0755)
%{_includedir}/*.h
%exclude %{_libdir}/libgdal.so.*
%exclude %{_libdir}/*.la
%{_libdir}/*

%files python
%defattr(-, root, root, 0755)
%{_bindir}/*.py
%{python_sitearch}/osgeo
%{python_sitearch}/GDAL-%{version}-py*.egg-info
%{python_sitearch}/osr.py*
%{python_sitearch}/ogr.py*
%{python_sitearch}/gdal*.py*

%changelog
