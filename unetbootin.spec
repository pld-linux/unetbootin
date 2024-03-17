Summary:	Create bootable Live USB drives for a variety of Linux distributions
Summary(pl.UTF-8):	Tworzenie rozruchowych urządzeń Live USB dla różnych dystrybucji Linuksa
Name:		unetbootin
Version:	657
Release:	1
License:	GPL v2+
Group:		Base
Source0:	https://github.com/unetbootin/unetbootin/releases/download/%{version}/%{name}-source-%{version}.tar.gz
# Source0-md5:	50ad69c1d703e635d30c3aa4305093f7
Patch0:		usb.patch
URL:		https://unetbootin.github.io/
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtNetwork-devel >= 4
BuildRequires:	desktop-file-utils
BuildRequires:	libstdc++-devel
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-linguist >= 4
BuildRequires:	qt4-qmake >= 4
Requires:	syslinux
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UNetbootin allows you to create bootable Live USB drives for a variety
of Linux distributions from Windows or Linux, without requiring you to
burn a CD. You can either let it download one of the many
distributions supported out-of-the-box for you, or supply your own
Linux .iso file if you've already downloaded one or your preferred
distribution isn't on the list.

%description -l pl.UTF-8
UNetbootin pozwala na tworzenie rozruchowych urządzeń USB z obrazami
Live dla różnych dystrybucji Linuksa z poziomu Windows lub Linuksa,
bez wymogu wypalania płyty CD. Nazędzie może samo pobrać jedną z wielu
dystrybucji obsługiwanych "out of the box", albo przyjąć dowolny,
wcześniej pobrany obraz .iso Linuksa, jeśli dystrybucji nie ma na
liście.

%prep
%setup -q -c
%patch0 -p1

sed -i '/^Version/d' unetbootin.desktop
sed -i '/\[en_US\]/d' unetbootin.desktop
sed -i 's|%{_bindir}/unetbootin|unetbootin|g' unetbootin.desktop

%build
export QTDIR=%{_prefix}/qt4
lupdate-qt4 unetbootin.pro
lrelease-qt4 unetbootin.pro
qmake-qt4 \
	"DEFINES += NOSTATIC" \
	"RESOURCES -= unetbootin.qrc"

%{__make} \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	CXXFLAGS="%{rpmcxxflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -D -p unetbootin $RPM_BUILD_ROOT%{_bindir}/unetbootin
# Install desktop file
desktop-file-install --vendor="" --remove-category=Application --dir=$RPM_BUILD_ROOT%{_desktopdir} unetbootin.desktop
# Install localization files
install -d $RPM_BUILD_ROOT%{_datadir}/unetbootin
install -p unetbootin_*.qm $RPM_BUILD_ROOT%{_datadir}/unetbootin
# Install pixmap
install -D -p unetbootin_512.png $RPM_BUILD_ROOT%{_pixmapsdir}/unetbootin.png

%find_lang %{name} --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.TXT
%attr(755,root,root) %{_bindir}/unetbootin
%dir %{_datadir}/unetbootin
%{_desktopdir}/unetbootin.desktop
%{_pixmapsdir}/unetbootin.png
