# TODO
# - gettext to system dir
%define		pkg	vshell
Summary:	Nagios V-Shell
Name:		nagios-%{pkg}
Version:	1.8
Release:	0.5
License:	GPL v2
Group:		Applications/WWW
Source0:	http://assets.nagios.com/downloads/exchange/nagiosvshell/%{pkg}.tar.gz
# Source0-md5:	802a80daa263b441af1b729cb3e7fa35
Source1:	apache.conf
Patch0:		config.patch
Patch1:		http-host.patch
URL:		http://exchange.nagios.org/directory/Addons/Frontends-(GUIs-and-CLIs)/Web-Interfaces/Nagios-V-2DShell/details
Requires:	nagios-cgi
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		nagios-%{pkg}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/nagios/%{pkg}

%description
Nagios V-Shell is a PHP web interface to Nagios Core that is designed
to be lightweight, easy to install and use, and customizable. V-Shell
has gettext support for internationalization.

%prep
# use versioned build dir
%setup -qc
mv %{pkg}/* .
%patch0 -p1
%patch1 -p1

# standard license
rm doc/gpl.txt

# we handle ourself the installation
mv install.php{,.sample}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -p *.php $RPM_BUILD_ROOT%{_appdir}
cp -a controllers css data js locale views $RPM_BUILD_ROOT%{_appdir}

cp -p config/vshell.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc INSTALL.txt doc/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{pkg}.conf
%{_appdir}
