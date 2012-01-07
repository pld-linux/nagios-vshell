# TODO
# - gettext to system dir
# - fixup config paths, like /etc/vshell.conf
%define		pkg	vshell
Summary:	Nagios V-Shell
Name:		nagios-%{pkg}
Version:	1.8
Release:	0.2
License:	GPL v2
Group:		Applications/WWW
Source0:	http://assets.nagios.com/downloads/exchange/nagiosvshell/%{pkg}.tar.gz
# Source0-md5:	802a80daa263b441af1b729cb3e7fa35
URL:		http://exchange.nagios.org/directory/Addons/Frontends-(GUIs-and-CLIs)/Web-Interfaces/Nagios-V-2DShell/details
Requires:	nagios-cgi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		nagios-%{pkg}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		appdir		%{_datadir}/nagios/%{pkg}

%description
Nagios V-Shell is a PHP web interface to Nagios Core that is designed
to be lightweight, easy to install and use, and customizable. V-Shell
has gettext support for internationalization.

%prep
# use versioned build dir
%setup -qc
mv %{pkg}/* .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{appdir}}
cp -p *.php $RPM_BUILD_ROOT%{appdir}
cp -a config controllers css data js locale views $RPM_BUILD_ROOT%{appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL.txt doc
%{appdir}
