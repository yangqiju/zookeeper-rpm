Name:           zookeeper
Version:        3.4.8
Release:        1%{?dist}
Summary:        zookeeper rpm test
Group:          Applications/System
License:        GPL
URL:            https://zookeeper.apache.org
Source0:        %{name}-%{version}.tar.gz 
Source1:	zookeeper.init
Source2:	zoo.cfg
BuildArch:	noarch
Provides:	zookeeper
Requires:	java >= 1.7
Requires(post):	/sbin/chkconfig,/sbin/service
Requires(preun): /sbin/chkconfig,/sbin/service


#BuildRequires:  
#Requires:       

%description

%define zookeeper_data_dir %{_datadir}/zookeeper
%define user zookeeper
%define group zookeeper
%define home /opt/zookeeper

%pre
getent group %{group} >/dev/null || groupadd -r %{group} 
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/zookeeper -s /sbin/nologin \
    -c "User for zookeeper services" %{user}
exit 0

%preun
/sbin/service zookeeper stop > /dev/null 2>&1
/sbin/chkconfig --del zookeeper > /dev/null 2>&1

%postun
rm -rf %{home}

%prep
%setup -q 

%build
#%%configure
#make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
echo 'install'
mkdir -p %{buildroot}%{home}
mkdir -p %{buildroot}/etc/init.d
mkdir -p %{buildroot}%{_localstatedir}/lib/zookeeper
mkdir -p %{buildroot}%{_var}/log/zookeeper
mkdir -p %{buildroot}%{zookeeper_data_dir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}%{_sysconfdir}/zookeeper
cp -R $RPM_BUILD_DIR/zookeeper-%{version}/* %{buildroot}%{home}
install -m 755 %{S:1} %{buildroot}%{_initrddir}/zookeeper 
install -D -p -m 644 %{S:2} %{buildroot}%{_sysconfdir}/zookeeper/



%post
#ls -sf %{buildroot}%{home}/bin/zkServer.sh %{buildroot}%{_sysconfdir}/init.d/zookeeper
/sbin/chkconfig zookeeper on
/sbin/service zookeeper start


%clean
rm -rf $RPM_BUILD_ROOT
echo 'clean'


%files
%defattr(-,root,root,-)
%doc
%{_initrddir}/zookeeper
%config %attr(-,%{user},%{group}) %{home}
%config %attr(-,%{user},%{group}) %{_sharedstatedir}/zookeeper
%config %attr(-,%{user},%{group}) %{_localstatedir}/log/zookeeper
%config %attr(-,%{user},%{group}) %{_sysconfdir}/zookeeper



%changelog
