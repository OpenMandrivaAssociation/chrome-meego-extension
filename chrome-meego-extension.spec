Name: chrome-meego-extension
Summary: The extension for Chrome Meego integration
Group: Applications/Internet
Version: 0.2.0
Release: %mkrel 1
License: LGPLv2.1
URL: https://www.meego.com/
Source0: http://repo.meego.com/MeeGo/releases/1.1/netbook/repos/source/%{name}-%{version}.tar.bz2
Source1: chromium-browser-ext.sh
Requires: python-simplejson
BuildRequires: python
BuildRequires: gnome-common
BuildRequires: intltool
BuildRequires: libglib2-devel
BuildRequires: libgtk+2-devel
BuildRequires: libxt-devel
BuildRequires: libGConf2-devel
BuildRequires: libsqlite3-devel
BuildRequires: zip
BuildRequires: openssl
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
The extension for Chrome MeeGo integration

%prep
%setup -q
%build
pushd plugin
../tools/gyp/gyp --depth=`pwd` -fmake
make %{?_smp_mflags}
mv out/Default/lib.target/libnpMeeGoPlugin.so ../extension/chrome-meego-extension/plugin
popd
pushd extension
python ../tools/crxmake/crxmake.py chrome-meego-extension chrome-meego-extension.pem chrome-meego-extension.crx
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/chrome-meego-extension/
cp -a extension/chrome-meego-extension.crx %{buildroot}%{_libdir}/chrome-meego-extension/
cp -a extension/external_extensions.json %{buildroot}%{_libdir}/chrome-meego-extension/
cp -a tools/installer %{buildroot}%{_libdir}/chrome-meego-extension/
mkdir -p %{buildroot}/usr/bin/
cp -a %{SOURCE1} %{buildroot}/usr/bin/
chmod 0755 %{buildroot}/usr/bin/chromium-browser-ext.sh

%clean
rm -rf %{buildroot}

%post
python /usr/lib/chrome-meego-extension/installer/installer.py install /usr/lib/chrome-meego-extension/external_extensions.json

%posttrans
python /usr/lib/chrome-meego-extension/installer/installer.py install /usr/lib/chrome-meego-extension/external_extensions.json

%preun
python /usr/lib/chrome-meego-extension/installer/installer.py uninstall /usr/lib/chrome-meego-extension/external_extensions.json

%files
%defattr(-,root,root,-)
/usr/lib/chrome-meego-extension
/usr/lib/chrome-meego-extension/chrome-meego-extension.crx
/usr/lib/chrome-meego-extension/external_extensions.json
/usr/bin/chromium-browser-ext.sh
