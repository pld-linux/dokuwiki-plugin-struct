%define		subver	2016-11-03
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		struct
%define		php_min_version 5.6.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki struct plugin
Summary(pl.UTF-8):	Wtyczka struct dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/cosmocode/dokuwiki-plugin-struct/archive/9ce9c74/%{plugin}-%{subver}.tar.gz
# Source0-md5:	7d6f2807334aa61515c22c430eee4749
URL:		https://www.dokuwiki.org/plugin:struct
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	dokuwiki >= 20160626
Requires:	dokuwiki-plugin-sqlite >= 20160810
Requires:	php(core) >= %{php_min_version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
A new structured data plugin.

This plugin draws heavy inspiration from the data plugin. It basically
tries to solve the same problem of assigning structured data to pages
and build automatic aggregations from it.

So why another plugin? The data plugin proved to be very useful and
versatile but had a few shortcomings:

- each page defined its own set of structured data
- there was no central way to ensure the structured data was
  consistent over multiple pages
- there was no easy way to modify the structured data set for multiple
  pages
- there was no validation for the data entered

%prep
%setup -qc
mv *-%{plugin}-*/{.??*,*} .

rm deleted.files
rm .travis.yml

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{LICENSE,README}
%{__rm} -r $RPM_BUILD_ROOT%{plugindir}/_test

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README LICENSE
%dir %{plugindir}
%{plugindir}/*.js
%{plugindir}/*.less
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/action
%{plugindir}/admin
%{plugindir}/conf
%{plugindir}/db
%{plugindir}/helper
%{plugindir}/jsoneditor
%{plugindir}/meta
%{plugindir}/renderer
%{plugindir}/script
%{plugindir}/syntax
%{plugindir}/types
