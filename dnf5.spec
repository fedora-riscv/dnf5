%global project_version_major 5
%global project_version_minor 0
%global project_version_patch 9

Name:           dnf5
Version:        5.0.9
Release:        1%{?dist}
Summary:        Command-line package manager
License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/dnf5
Source0:        %{url}/archive/%{version}/dnf5-%{version}.tar.gz

Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       dnf-data
Recommends:     bash-completion

# Remove if condition when Fedora 37 is EOL
%if 0%{?fedora} > 37
Provides:       microdnf = %{version}-%{release}
Obsoletes:      microdnf < 4
%endif

# ========== build options ==========

%bcond_without dnf5daemon_client
%bcond_without dnf5daemon_server
%bcond_without libdnf_cli
%bcond_without dnf5
%bcond_without dnf5_plugins
%bcond_without plugin_actions
%bcond_without python_plugins_loader

%bcond_without comps
%bcond_without modulemd
%bcond_without zchunk

%bcond_with    html
%if 0%{?rhel} == 8
%bcond_with    man
%else
%bcond_without man
%endif

# TODO Go bindings fail to build, disable for now
%bcond_with    go
%bcond_without perl5
%bcond_without python3
%bcond_without ruby

%bcond_with    clang
%bcond_with    sanitizers
%bcond_without tests
%bcond_with    performance_tests
%bcond_with    dnf5daemon_tests

%if %{with clang}
    %global toolchain clang
%endif

# ========== versions of dependencies ==========

%global libmodulemd_version 2.5.0
%global librepo_version 1.15.0
%global libsolv_version 0.7.21
%global sqlite_version 3.35.0
%global swig_version 4
%global zchunk_version 0.9.11


# ========== build requires ==========

BuildRequires:  bash-completion
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gettext
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(fmt)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(librepo) >= %{librepo_version}
BuildRequires:  pkgconfig(libsolv) >= %{libsolv_version}
BuildRequires:  pkgconfig(libsolvext) >= %{libsolv_version}
BuildRequires:  pkgconfig(rpm) >= 4.17.0
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
BuildRequires:  toml11-static

%if %{with clang}
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
%endif

%if %{with tests}
BuildRequires:  createrepo_c
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  rpm-build
%endif

%if %{with comps}
BuildRequires:  pkgconfig(libcomps)
%endif

%if %{with modulemd}
BuildRequires:  pkgconfig(modulemd-2.0) >= %{libmodulemd_version}
%endif

%if %{with zchunk}
BuildRequires:  pkgconfig(zck) >= %{zchunk_version}
%endif

%if %{with html} || %{with man}
BuildRequires:  python3dist(breathe)
BuildRequires:  python3dist(sphinx) >= 4.1.2
BuildRequires:  python3dist(sphinx-rtd-theme)
%endif

%if %{with sanitizers}
# compiler-rt is required by sanitizers in clang
BuildRequires:  compiler-rt
BuildRequires:  libasan
BuildRequires:  liblsan
BuildRequires:  libubsan
%endif

%if %{with libdnf_cli}
# required for libdnf5-cli
BuildRequires:  pkgconfig(smartcols)
%endif

%if %{with dnf5daemon_server}
# required for dnf5daemon-server
BuildRequires:  pkgconfig(sdbus-c++) >= 0.8.1
BuildRequires:  systemd-rpm-macros
%if %{with dnf5daemon_tests}
BuildRequires:  dbus-daemon
BuildRequires:  polkit
BuildRequires:  python3-devel
BuildRequires:  python3dist(dbus-python)
%endif
%endif

# ========== language bindings section ==========

%if %{with perl5} || %{with ruby} || %{with python3}
BuildRequires:  swig >= %{swig_version}
%endif

%if %{with perl5}
# required for perl-libdnf5 and perl-libdnf5-cli
BuildRequires:  perl-devel
BuildRequires:  perl-generators
%if %{with tests}
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(warnings)
%endif
%endif

%if %{with ruby}
# required for ruby-libdnf5 and ruby-libdnf5-cli
BuildRequires:  pkgconfig(ruby)
%if %{with tests}
BuildRequires:  rubygem-test-unit
%endif
%endif

%if %{with python3}
# required for python3-libdnf5 and python3-libdnf5-cli
BuildRequires:  python3-devel
%endif

%description
DNF5 is a command-line package manager that automates the process of installing,
upgrading, configuring, and removing computer programs in a consistent manner.
It supports RPM packages, modulemd modules, and comps groups & environments.

%files
%{_bindir}/dnf5

# Remove if condition when Fedora 37 is EOL
%if 0%{?fedora} > 37
%{_bindir}/microdnf
%endif

%dir %{_sysconfdir}/dnf/dnf5-aliases.d
%doc %{_sysconfdir}/dnf/dnf5-aliases.d/README
%dir %{_datadir}/dnf5
%dir %{_datadir}/dnf5/aliases.d
%config %{_datadir}/dnf5/aliases.d/compatibility.conf
%dir %{_libdir}/dnf5
%dir %{_libdir}/dnf5/plugins
%doc %{_libdir}/dnf5/plugins/README
%dir %{_libdir}/libdnf5/plugins
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/dnf5
%dir %{_prefix}/lib/sysimage/dnf
%verify(not md5 size mtime) %ghost %{_prefix}/lib/sysimage/dnf/*
%license COPYING.md
%license gpl-2.0.txt
%{_mandir}/man8/dnf5.8.*
%{_mandir}/man8/dnf5-advisory.8.*
%{_mandir}/man8/dnf5-clean.8.*
%{_mandir}/man8/dnf5-distro-sync.8.*
%{_mandir}/man8/dnf5-downgrade.8.*
%{_mandir}/man8/dnf5-download.8.*
%{_mandir}/man8/dnf5-environment.8.*
%{_mandir}/man8/dnf5-group.8.*
# TODO(jkolarik): history is not ready yet
# %%{_mandir}/man8/dnf5-history.8.*
%{_mandir}/man8/dnf5-install.8.*
%{_mandir}/man8/dnf5-leaves.8.*
%{_mandir}/man8/dnf5-makecache.8.*
%{_mandir}/man8/dnf5-mark.8.*
# TODO(jkolarik): module is not ready yet
# %%{_mandir}/man8/dnf5-module.8.*
%{_mandir}/man8/dnf5-reinstall.8.*
%{_mandir}/man8/dnf5-remove.8.*
%{_mandir}/man8/dnf5-repo.8.*
%{_mandir}/man8/dnf5-repoquery.8.*
%{_mandir}/man8/dnf5-search.8.*
%{_mandir}/man8/dnf5-swap.8.*
%{_mandir}/man8/dnf5-upgrade.8.*
%{_mandir}/man7/dnf5-comps.7.*
# TODO(jkolarik): filtering is not ready yet
# %%{_mandir}/man7/dnf5-filtering.7.*
%{_mandir}/man7/dnf5-installroot.7.*
# TODO(jkolarik): modularity is not ready yet
# %%{_mandir}/man7/dnf5-modularity.7.*
%{_mandir}/man7/dnf5-specs.7.*

# ========== libdnf5 ==========
%package -n libdnf5
Summary:        Package management library
License:        LGPL-2.1-or-later
#Requires:       libmodulemd{?_isa} >= {libmodulemd_version}
Requires:       libsolv%{?_isa} >= %{libsolv_version}
Requires:       librepo%{?_isa} >= %{librepo_version}
Requires:       sqlite-libs%{?_isa} >= %{sqlite_version}

%description -n libdnf5
Package management library.

%files -n libdnf5
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so.1*
%license lgpl-2.1.txt
%{_var}/cache/libdnf/

# ========== libdnf5-cli ==========

%if %{with libdnf_cli}
%package -n libdnf5-cli
Summary:        Library for working with a terminal in a command-line package manager
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli
Library for working with a terminal in a command-line package manager.

%files -n libdnf5-cli
%{_libdir}/libdnf-cli.so.1*
%license COPYING.md
%license lgpl-2.1.txt
%endif

# ========== dnf5-devel ==========

%package -n dnf5-devel
Summary:        Development files for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-devel%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli-devel%{?_isa} = %{version}-%{release}

%description -n dnf5-devel
Develpment files for dnf5.

%files -n dnf5-devel
%{_includedir}/dnf5/
%license COPYING.md
%license lgpl-2.1.txt


# ========== libdnf5-devel ==========

%package -n libdnf5-devel
Summary:        Development files for libdnf
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libsolv-devel%{?_isa} >= %{libsolv_version}
Conflicts:      libdnf-devel < 5

%description -n libdnf5-devel
Development files for libdnf.

%files -n libdnf5-devel
%{_includedir}/libdnf/
%dir %{_libdir}/libdnf5
%{_libdir}/libdnf5.so
%{_libdir}/pkgconfig/libdnf.pc
%license COPYING.md
%license lgpl-2.1.txt


# ========== libdnf5-cli-devel ==========

%package -n libdnf5-cli-devel
Summary:        Development files for libdnf5-cli
License:        LGPL-2.1-or-later
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n libdnf5-cli-devel
Development files for libdnf5-cli.

%files -n libdnf5-cli-devel
%{_includedir}/libdnf-cli/
%{_libdir}/libdnf-cli.so
%{_libdir}/pkgconfig/libdnf-cli.pc
%license COPYING.md
%license lgpl-2.1.txt


# ========== perl-libdnf5 ==========

%if %{with perl5}
%package -n perl-libdnf5
Summary:        Perl 5 bindings for the libdnf library
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}


%description -n perl-libdnf5
Perl 5 bindings for the libdnf library.

%files -n perl-libdnf5
%{perl_vendorarch}/libdnf5
%{perl_vendorarch}/auto/libdnf5
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== perl-libdnf5-cli ==========

%if %{with perl5} && %{with libdnf_cli}
%package -n perl-libdnf5-cli
Summary:        Perl 5 bindings for the libdnf5-cli library
License:        LGPL-2.1-or-later
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}


%description -n perl-libdnf5-cli
Perl 5 bindings for the libdnf5-cli library.

%files -n perl-libdnf5-cli
%{perl_vendorarch}/libdnf5_cli
%{perl_vendorarch}/auto/libdnf5_cli
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== python3-libdnf5 ==========

%if %{with python3}
%package -n python3-libdnf5
%{?python_provide:%python_provide python3-libdnf}
Summary:        Python 3 bindings for the libdnf library
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5
Python 3 bindings for the libdnf library.

%files -n python3-libdnf5
%{python3_sitearch}/libdnf5
%{python3_sitearch}/libdnf5-*.dist-info
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== python3-libdnf5-cli ==========

%if %{with python3} && %{with libdnf_cli}
%package -n python3-libdnf5-cli
%{?python_provide:%python_provide python3-libdnf5-cli}
Summary:        Python 3 bindings for the libdnf5-cli library
License:        LGPL-2.1-or-later
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-cli
Python 3 bindings for the libdnf5-cli library.

%files -n python3-libdnf5-cli
%{python3_sitearch}/libdnf5_cli
%{python3_sitearch}/libdnf5_cli-*.dist-info
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== ruby-libdnf5 ==========

%if %{with ruby}
%package -n ruby-libdnf5
Summary:        Ruby bindings for the libdnf library
License:        LGPL-2.1-or-later
Provides:       ruby(libdnf) = %{version}-%{release}
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       ruby(release)

%description -n ruby-libdnf5
Ruby bindings for the libdnf library.

%files -n ruby-libdnf5
%{ruby_vendorarchdir}/libdnf5
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== ruby-libdnf5-cli ==========

%if %{with ruby} && %{with libdnf_cli}
%package -n ruby-libdnf5-cli
Summary:        Ruby bindings for the libdnf5-cli library
License:        LGPL-2.1-or-later
Provides:       ruby(libdnf_cli) = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       ruby(release)

%description -n ruby-libdnf5-cli
Ruby bindings for the libdnf5-cli library.

%files -n ruby-libdnf5-cli
%{ruby_vendorarchdir}/libdnf5_cli
%license COPYING.md
%license lgpl-2.1.txt
%endif


# ========== libdnf5-plugin-actions ==========

%if %{with plugin_actions}
%package -n libdnf5-plugin-actions
Summary:        Libdnf plugin that allows to run actions (external executables) on hooks
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}

%description -n libdnf5-plugin-actions
Libdnf plugin that allows to run actions (external executables) on hooks.

%files -n libdnf5-plugin-actions
%{_libdir}/libdnf5/plugins/actions.*
%endif


# ========== python3-libdnf5-plugins-loader ==========

%if %{with python_plugins_loader}
%package -n python3-libdnf5-python-plugins-loader
Summary:        Libdnf plugin that allows loading Python plugins
License:        LGPL-2.1-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       python3-libdnf5%{?_isa} = %{version}-%{release}

%description -n python3-libdnf5-python-plugins-loader
Libdnf plugin that allows loading Python plugins.

%files -n python3-libdnf5-python-plugins-loader
%{_libdir}/libdnf5/plugins/python_plugins_loader.*
%dir %{python3_sitelib}/libdnf_plugins/
%doc %{python3_sitelib}/libdnf_plugins/README
%endif


# ========== dnf5daemon-client ==========

%if %{with dnf5daemon_client}
%package -n dnf5daemon-client
Summary:        Command-line interface for dnf5daemon-server
License:        GPL-2.0-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       dnf5daemon-server

%description -n dnf5daemon-client
Command-line interface for dnf5daemon-server.

%files -n dnf5daemon-client
%{_bindir}/dnf5daemon-client
%license COPYING.md
%license gpl-2.0.txt
%{_mandir}/man8/dnf5daemon-client.8.*
%endif


# ========== dnf5daemon-server ==========

%if %{with dnf5daemon_server}
%package -n dnf5daemon-server
Summary:        Package management service with a DBus interface
License:        GPL-2.0-or-later
Requires:       libdnf5%{?_isa} = %{version}-%{release}
Requires:       libdnf5-cli%{?_isa} = %{version}-%{release}
Requires:       dbus
Requires:       dnf-data
Requires:       polkit

%description -n dnf5daemon-server
Package management service with a DBus interface.

%post -n dnf5daemon-server
%systemd_post dnf5daemon-server.service

%preun -n dnf5daemon-server
%systemd_preun dnf5daemon-server.service

%postun -n dnf5daemon-server
%systemd_postun_with_restart dnf5daemon-server.service

%files -n dnf5daemon-server
%{_sbindir}/dnf5daemon-server
%{_unitdir}/dnf5daemon-server.service
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.rpm.dnf.v0.conf
%{_datadir}/dbus-1/system-services/org.rpm.dnf.v0.service
%{_datadir}/dbus-1/interfaces/org.rpm.dnf.v0.*.xml
%{_datadir}/polkit-1/actions/org.rpm.dnf.v0.policy
%license COPYING.md
%license gpl-2.0.txt
%{_mandir}/man8/dnf5daemon-server.8.*
%{_mandir}/man8/dnf5daemon-dbus-api.8.*
%endif


# ========== dnf5-plugins ==========

%if %{with dnf5_plugins}
%package -n dnf5-plugins
Summary:        Plugins for dnf5
License:        LGPL-2.1-or-later
Requires:       dnf5%{?_isa} = %{version}-%{release}

%description -n dnf5-plugins
Core DNF5 plugins that enhance dnf5 with builddep and changelog commands.

%files -n dnf5-plugins
%{_libdir}/dnf5/plugins/*.so
%endif


# ========== unpack, build, check & install ==========

%prep
%autosetup -p1 -n dnf5-%{version}


%build
%cmake \
    -DPACKAGE_VERSION=%{version} \
    -DPERL_INSTALLDIRS=vendor \
    \
    -DWITH_DNF5DAEMON_CLIENT=%{?with_dnf5daemon_client:ON}%{!?with_dnf5daemon_client:OFF} \
    -DWITH_DNF5DAEMON_SERVER=%{?with_dnf5daemon_server:ON}%{!?with_dnf5daemon_server:OFF} \
    -DWITH_LIBDNF5_CLI=%{?with_libdnf_cli:ON}%{!?with_libdnf_cli:OFF} \
    -DWITH_DNF5=%{?with_dnf5:ON}%{!?with_dnf5:OFF} \
    -DWITH_PLUGIN_ACTIONS=%{?with_plugin_actions:ON}%{!?with_plugin_actions:OFF} \
    -DWITH_PYTHON_PLUGINS_LOADER=%{?with_python_plugins_loader:ON}%{!?with_python_plugins_loader:OFF} \
    \
    -DWITH_COMPS=%{?with_comps:ON}%{!?with_comps:OFF} \
    -DWITH_MODULEMD=%{?with_modulemd:ON}%{!?with_modulemd:OFF} \
    -DWITH_ZCHUNK=%{?with_zchunk:ON}%{!?with_zchunk:OFF} \
    \
    -DWITH_HTML=%{?with_html:ON}%{!?with_html:OFF} \
    -DWITH_MAN=%{?with_man:ON}%{!?with_man:OFF} \
    \
    -DWITH_GO=%{?with_go:ON}%{!?with_go:OFF} \
    -DWITH_PERL5=%{?with_perl5:ON}%{!?with_perl5:OFF} \
    -DWITH_PYTHON3=%{?with_python3:ON}%{!?with_python3:OFF} \
    -DWITH_RUBY=%{?with_ruby:ON}%{!?with_ruby:OFF} \
    \
    -DWITH_SANITIZERS=%{?with_sanitizers:ON}%{!?with_sanitizers:OFF} \
    -DWITH_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
    -DWITH_PERFORMANCE_TESTS=%{?with_performance_tests:ON}%{!?with_performance_tests:OFF} \
    -DWITH_DNF5DAEMON_TESTS=%{?with_dnf5daemon_tests:ON}%{!?with_dnf5daemon_tests:OFF} \
    \
    -DPROJECT_VERSION_MAJOR=%{project_version_major} \
    -DPROJECT_VERSION_MINOR=%{project_version_minor} \
    -DPROJECT_VERSION_PATCH=%{project_version_patch}
%cmake_build
%if %{with man}
    %cmake_build --target doc-man
%endif


%check
%if %{with tests}
    %ctest
%endif


%install
%cmake_install

# own dirs and files that dnf5 creates on runtime
mkdir -p %{buildroot}%{_prefix}/lib/sysimage/dnf
for files in \
    groups.toml modules.toml nevras.toml packages.toml \
    system.toml transaction_history.sqlite \
    transaction_history.sqlite-shm \
    transaction_history.sqlite-wal userinstalled.toml
do
    touch %{buildroot}%{_prefix}/lib/sysimage/dnf/$files
done

#find_lang {name}

# Remove if condition when Fedora 37 is EOL
%if 0%{?fedora} > 37
ln -sr %{buildroot}%{_bindir}/dnf5 %{buildroot}%{_bindir}/microdnf
%endif

%ldconfig_scriptlets


%changelog
* Wed Apr 26 2023 Nicola Sella <nsella@redhat.com> - 5.0.9-1
- Release 5.0.9 (Nicola Sella)
- Fix packit configuration (Nicola Sella)
- solv_repo: Do not keep comps solvables ranges (Marek Blaha)
- repo_sack: Fix missing xml files for installed groups (Marek Blaha)
- solv_repo: Create group solvable from system state (Marek Blaha)
- solv_repo: Method to read group solvable from xml (Marek Blaha)
- comps: Handle error while serializing group (Marek Blaha)
- solv_repo: Keep track of groups without xml (Marek Blaha)
- repo: Set also repo in comps_pool as installed (Marek Blaha)
- dnf5] Add "--userinstalled" to "repoquery" man page (Jaroslav Rohel)
- [dnf5] Support for "--userinstalled" argument in repoquery (Jaroslav Rohel)
- Add packit action to do auto-release (Nicola Sella)
- progressbar: Prevent length_error exception (RhBug:2184271) (Marek Blaha)
- [doc] project layout: Add dnf5-plugins directory (Jaroslav Rohel)
- [doc] Coding style: Use C++20 (Jaroslav Rohel)
- Fix .clang-format: Replace Cpp11 with c++20 (Jaroslav Rohel)
- [dnf5] Add "--leaves" to "repoquery" man page (Jaroslav Rohel)
- [dnf5] Add man page for leaves command (Jaroslav Rohel)
- [dnf5] Support for "--leaves" argument in "repoquery" command (Jaroslav Rohel)
- [dnf5] leaves command: Add long description (Jaroslav Rohel)
- [dnf5] Command leaves (Jaroslav Rohel)
- swig: Add VectorPackage and VectorVectorPackage templates (Jaroslav Rohel)
- Implement new filters rpm::filter_leaves and rpm::filter_leaves_groups (Jaroslav Rohel)
- Release 5.0.8 (Nicola Sella)
- [dnf5] Improve error message in download command (Jaroslav Rohel)
- [dnf5] Fix help in case argument parser detect error (Jaroslav Rohel)
- generate dist-info for Python bindings (Matt Davis)
- package_sack: Fix running kernel logging (Marek Blaha)
- repoquery: unify option descriptions (Aleš Matěj)
- repoquery: add --latest-limit option (Aleš Matěj)
- Add 4 aliases for dnf5 commands (Jaroslav Mracek)
- modules: Rename ModuleState enum to ModuleStatus (Pavla Kratochvilova)
- Include base_weak.hpp because of base getters (Aleš Matěj)
- Silent Swig Python memory leak/no destructor find (Aleš Matěj)
- Update Python API test to check LogEvent::get_spec() wrapper (Jan Kolarik)
- swig: Add wrapper for string pointers (Jan Kolarik)
- Add Python API tests for LogEvent wrappers (Jan Kolarik)
- swig: Add bindings for LogEvent (Jan Kolarik)
- [dnf5] Add "up" and "update" aliases for "upgrade" command (Jaroslav Rohel)
- NullLogger::write: Fix type of time argument (Jaroslav Rohel)
- doc: Add info about package spec expressions (RhBug:2160420) (Jan Kolarik)
- repoquery: add formatting options --requires, --provides.. (Aleš Matěj)
- repoquery: remove unused nevra option (Aleš Matěj)
- repoquery: add formatting func for attr options --requires/--provides.. (Aleš Matěj)
- tests: `print_pkg_set_with_format(..)` in repoquery (Aleš Matěj)
- tests: move test helpers into a shared library (Aleš Matěj)
- repoquery: use queryformat str to format output for pkgs (Aleš Matěj)
- repoquery: add `--queryformat` option (Aleš Matěj)
- dnf5: Fix total number of actions (bars) in transaction progress (Jaroslav Rohel)
- Add method API base::Transaction::get_transaction_packages_count (Jaroslav Rohel)
- MultiProgressBar: get/set total number of bars (Jaroslav Rohel)
- dnf5: Hide total transaction progress bar (Jaroslav Rohel)
- MultiProgressBar: Define constexpr NEVER_VISIBLE_LIMIT (Jaroslav Rohel)
- Deduplicate installroot config logic (Evan Goode)
- Correctly load repos from installroot config file (Evan Goode)
- repo::RepoSack::update_and_load_repos: Do not download local key files (Jaroslav Rohel)
- repo::RepoSack::update_and_load_repos: Use FileDownloader to download keys (Jaroslav Rohel)
- repo::RepoSack::update_and_load_repos: Arg to enable/disable keys import (Jaroslav Rohel)
- repo::RepoSack::update_and_load_repos: Process repos with bad keys last (Jaroslav Rohel)
- RepoSack::update_and_load_repos: First load repositories from cache (Jaroslav Rohel)
- repo::Repo::get_config: Add const version of method (Jaroslav Rohel)
- RepoDownloader::reset_loaded (Jaroslav Rohel)
- modules: Change State to set and get the whole ModuleState (Pavla Kratochvilova)
- dnf5: Stats: total and downloaded pkgs size, installed and freed space (Jaroslav Rohel)
- dnf5::Context::print_info: Make method const and public (Jaroslav Rohel)
- cli::utils::units: Add `to_size` func, rename `format_size` func (Jaroslav Rohel)
- cli::utils::units::format_size: Fix formatting of negative numbers (Jaroslav Rohel)
- New API method rpm::Package::is_available_locally (Jaroslav Rohel)
- Create utils::OnScopeExit template class (Jaroslav Rohel)
- Command::get_parent_command(): return the real parent (Pavel Raiskup)
- Move description of DNF5 changes to doc (Jaroslav Mracek)
- RepoSack: remember the repo file path (Pavel Raiskup)
- pep8 fix in the tests (Marek Blaha)
- dnfdaemon: Test install of rpm file from path (Marek Blaha)
- dnfdaemon: Transaction commands work with file paths (Marek Blaha)
- dnfdaemon-client: Unify pkg_specs argument across commands (Marek Blaha)
- dnf5daemon-client: Command line args parsing as dnf5 (Marek Blaha)
- dnfdaemon: Remove unused includes (Marek Blaha)
- dnfdaemon: Test for goal (Marek Blaha)
- dnfdaemon: Handle errors with unresolved transaction usage (Marek Blaha)
- Use repo::DownloadCallbacks for all downloads (Jaroslav Rohel)
- MultiProgressBar: Methods to hide total bar and its number widget (Jaroslav Rohel)
- Mark DownloadProgressBar::set_number_vidget_visible as noexcept (Jaroslav Rohel)
- Add Python API tests for load_extra_system_repo bad usages (Jan Kolarik)
- repo: Use API assertions on API (Jan Kolarik)
- Add Python API test for duplicate global logger instances (Jan Kolarik)
- global_logger: Use API assertion (Jan Kolarik)
- Add Python API tests for configuration locking (Jan Kolarik)
- conf: Throw API assertions for Option methods (Jan Kolarik)
- Add Python API tests for unsupported arguments in goal (Jan Kolarik)
- goal: Use API assertion for unsupported argument (Jan Kolarik)
- Add Python API tests for goal resolving use cases (Jan Kolarik)
- swig: Convert all API assertions and runtime errors to SWIG runtime errors (Jan Kolarik)
- transaction: Fix impl constructor (Jan Kolarik)
- GoalPrivate: Fix protecting the running kernel (Marek Blaha)
- goal: Better handling of obsoleted pkg installation (Marek Blaha)
- PackageQuery: New ctor based on the PackageSet instance (Marek Blaha)
- search: Fix typo from the previous commit (Jan Kolarik)
- Remove showdupesfromrepos config option (Marek Blaha)
- Fix files with pre-comit (Nicola Sella)
- Add pre-commit to github actions (Nicola Sella)
- Remove clang-format workflow (Nicola Sella)
- Fix a typo in sqlite Requires in dnf5.spec (Petr Písař)
- Set a minimal sqlite version (Petr Písař)
- man: Add info about download command destination (Jan Kolarik)
- output: Print resolve logs to stderr (Marek Blaha)
- Add rpmlint to precommit (Nicola Sella)
- dnf5daemon-server: Fix system repo double loading (Marek Blaha)
- dnf5daemon-client: Remove unused method (Marek Blaha)
- Add capability to find binaries to resolve_spec (Jaroslav Mracek)
- Add global logger Python API test (Jan Kolarik)
- swig: Add bindings for global logger (Jan Kolarik)
- Add file logger factory Python API tests (Jan Kolarik)
- swig: Add bindings for file logger factory (Jan Kolarik)
- Add file logger factory C++ API tests (Jan Kolarik)
- main: Use new factory for file logging (Jan Kolarik)
- logger: Add factory method for creating file logger (Jan Kolarik)
- goal: Fix group packages removal (RhBug:2173927) (Marek Blaha)
- :Basic pre-commit configuration (Jiri Podivin)
- solv_repo: Fix creating solver cache for comps (RhBug:2173929) (Jan Kolarik)
- Fix a couple of memory leaks (Aleš Matěj)
- Change to --use-host-config, warning suggesting --use-host-config (Evan Goode)
- Load config and reposdir from installroot (Evan Goode)
- Change Python scripts to use new configuration attributes (Jan Kolarik)
- Add Python API tests for new configuration attributes (Jan Kolarik)
- swig: Add shortcuts for configuration options in Python (Jan Kolarik)
- conf: Rename option getters (Jan Kolarik)
- Revert "conf: New configuration option "disable_multithreading"" (Jaroslav Rohel)
- Revert "RepoSack::update_and_load_repos: Added single-threaded mode" (Jaroslav Rohel)
- Unit tests: Enable multithreading (Jaroslav Rohel)
- Disable parallel running of some unit tests (Jaroslav Rohel)
- conf: Change default color of installed pkg version (Marek Blaha)
- Describe the changes in the list command behavior (Marek Blaha)
- dnf5: Add compatibility alias ls->list (Marek Blaha)
- dnf5: Implement info command (Marek Blaha)
- dnf5: Implement list command (Marek Blaha)
- libdnf-cli: Packages info by sections (Marek Blaha)
- libdnf-cli: Output of package lists by sections (Marek Blaha)
- libdnf-cli: Class for colorizing list output (Marek Blaha)
- dnf5: Fix --exactdeps argument description (Marek Blaha)

* Thu Apr 13 2023 Nicola Sella <nsella@redhat.com> - 5.0.8-1
- Update to 5.0.8
- Improve error message in download command
- Add repoquery --latest-limit option
- Add dg, in, rei, rm aliases
- Add "up" and "update" aliases for "upgrade" command
- Update documentation with info about package spec expressions (RhBug:2160420)
- Add formatting options repoquery --requires, --provides..
- Remove unused repoquery nevra option
- Add `--queryformat` option to repoquery
- Improved progress bars
- Fix logic of installroot with deduplication
- Correctly load repos from installroot config file
- Improved loading and downloading of key files
- Improved modules: Change State to set and get the whole ModuleState
- New API method rpm::Package::is_available_locally
- Move description of DNF5 changes to doc
- Improved dnf5daemon logic and removed unused code
- Improved progress bar
- Improved handling of obsolete package installation
- Remove showdupesfromrepos config option
- man: Add info about download command destination
- Print resolve logs to stderr
- Fix double loading of system repo in dnf5daemon
- Set a minimal sqlite version
- Change to --use-host-config, warning suggesting --use-host-config
- Add capability to find binaries to resolve_spec
- Add pre-commit file
- Improved by fixing memory leaks
- Improved tests by enabling with multithreading
- Improve documentation  for list command
- Add compatibility alias ls->list
- Implement info command
- Implement list command
- Fix --exactdeps argument description

* Wed Mar 8 2023 Nicola Sella <nsella@redhat.com> - 5.0.7-1
- Document set/get vars in python api
- Document --strict deprecation
- New configuration option "disable_multithreading"
- Improved dnf5daemon to handle support groups and modules in return value
- Ignore inaccessible config unless path specified as --config=...
- Includes reordering and tweaks in advisories
- Add support for package changelogs in swig and tests
- Add many unit tests for dnf5 and python api
- Add new --skip-unavailable command line option
- Add search command
- Add new error for incorrect API usages
- Add a new method whether base was correctly initialized
- Improved python exceptions on undefined var
- transaction: Change API to run transaction without args
- Add explicit package version for libdnf5-cli
- Improved performance of packagequery

* Tue Feb 14 2023 Nicola Sella <nsella@redhat.com> - 5.0.6-1
- Add obsoletes of microdnf
- Many improvements related to internal logic and bugfixes
- Improvements in specfile
- Improved API, drop std::optional
- Use Autoapi instead of Autodoc to generate Python docs
- Improved documentation for modules

* Thu Jan 26 2023 Nicola Sella <nsella@redhat.com> - 5.0.5-1
- Fix build fail in rawhide
- Fixes in the concerning filesystem
- Fixes in the concerning modules
- Fixes in the concerning api

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Nicola Sella <nsella@redhat.com> - 5.0.4-2
- Backport downstream patch to disable unit tests for python tutorials
- Fix build in rawhide

* Thu Jan 12 2023 Nicola Sella <nsella@redhat.com> - 5.0.4-1
- Many fixes in perl bindings
- Test functions enhanced
- Extend unit tests for OptionString and OptionStringList

* Wed Jan 04 2023 Nicola Sella <nsella@redhat.com> - 5.0.3-1
- Add Python docs for: Base, Goal, RepoQuery, Package and PackageQuery
- Add docs for Python bindings: they are auto generated now
- Add --what* and --exactdeps options to repoquery
- Add "user enter password" to dnf5daemon functionalities
- Fix: remove repeating headers in transaction table
- Fix: Set status of download progress bar after successful download
- Fix: RepoDownloader::get_cache_handle: Don't set callbacks in LibrepoHandle
- Refactor internal utils
- Improved GlobalLogger
- Improved C++ API docs

* Thu Dec 08 2022 Nicola Sella <nsella@redhat.com> - 5.0.2-1
- Implement group remove command
- Improved options in config
- Add support for any number of user IDs in a PGP key
- Use new librepo PGP API
- remove gpgme dependency
- Improved exceptions and dnf5 errors
- Add dnf5-devel package
- Update README.md with up to date information
- Repoquery: Add --duplicates option
- Improved documentation for Repoquery, Upgrande and About section
- Add tutorials for python3 bindings
- dnf5-changes-doc: Add more structure using different headings
- Add ModuleQuery
- Improvements in comps logic

* Fri Nov 25 2022 Nicola Sella <nsella@rehat.com> - 5.0.1-1
- Update to 5.0.1
- Fix loading known keys for RepoGpgme
- Fix dnf5 progress_bar
- Improve modules: conflicting packages, weak resolve, active modules resolving
- plugins.hpp moved away from public headers and improvements logic
- Fix failing builds for i686 arch
- Add man pages to dnf5
- Fix non x86_64 builds
- Remove unimplemented commands

* Wed Nov 2 2022 Nicola Sella <nsella@redhat.com> - 5.0.0-2~pre
- Fix failing builds for i686 arch

* Mon Oct 31 2022 Nicola Sella <nsella@redhat.com> - 5.0.0-1~pre
- Add man pages to dnf5
- Fix non x86_64 builds
- Remove unimplemented commands

* Fri Sep 16 2022 Nicola Sella - <nsella@redhat.com> - 5.0.0-0~pre
- Dnf pre release build for Fedora
