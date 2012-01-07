# TODO
# - gettext to system dir
%define		pkg	vshell
%define		php_min_version 5.2.0
%include	/usr/lib/rpm/macros.php
Summary:	Nagios V-Shell
Name:		nagios-%{pkg}
Version:	1.8
Release:	0.8
License:	GPL v2
Group:		Applications/WWW
Source0:	http://assets.nagios.com/downloads/exchange/nagiosvshell/%{pkg}.tar.gz
# Source0-md5:	802a80daa263b441af1b729cb3e7fa35
Patch0:		config.patch
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
Patch1:		http-host.patch
URL:		http://exchange.nagios.org/directory/Addons/Frontends-(GUIs-and-CLIs)/Web-Interfaces/Nagios-V-2DShell/details
Requires:	nagios-cgi
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-date
Requires:	php-gettext
Requires:	php-json
Requires:	php-pcre
Requires:	php-session
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php-pecl-APC >= 3.0.13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_sysconfdir	%{_webapps}/nagios
%define		_appdir		%{_datadir}/nagios/%{pkg}

# bad depsolver
%define		_noautopear	pear
# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL.txt doc/*
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{pkg}.conf
%{_appdir}
