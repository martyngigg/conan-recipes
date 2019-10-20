from conans import AutoToolsBuildEnvironment, ConanFile, tools


class PythonConan(ConanFile):
    name = "Python"
    version = "3.8.0"
    license = "MIT"
    author = "Martyn Gigg <martyn.gigg@gmail.com>"
    description = "Official interpreter of Python language"
    url = "https://github.com/martyngigg/conan-recipes.git"
    topics = ("cpython", )
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    generators = "make"
    build_requires = (\
      "zlib/1.2.11",
      "openssl/1.1.1d@_/_",
      "libffi/3.2.1@bincrafters/stable"
    )

    # Private variables
    _build_vars = ""

    def source(self):
        source_url = "https://www.python.org/ftp/python/"
        tools.get(source_url + "{version}/Python-{version}.tar.xz".format(
            version=self.version))

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        build_vars = autotools.vars
        build_vars["LDFLAGS"] += " -Wl,-rpath,'$$ORIGIN/../lib'"
        self._build_vars = build_vars
        flags = [
            "--enable-shared", "--enable-ipv6",
            "--enable-loadable-sqlite-extensions",
            "--with-dbmliborder=bdb:gdbm", "--with-computed-gotos",
            "--without-ensurepip",
            "--with-openssl={}".format(self.deps_cpp_info["openssl"].rootpath)
        ]
        autotools.configure(configure_dir="Python-{}".format(self.version),
                            args=flags,
                            vars=build_vars)
        autotools.make(vars=build_vars)

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.make(target="install", vars=self._build_vars)

    def package_info(self):
        major_version, minor_version = self.version.split(".")[0:2]
        python_x_y = "python{}.{}".format(major_version, minor_version)
        self.cpp_info.includedirs = ["include/" + python_x_y]
        self.cpp_info.libs = ["lib{}.so".format(python_x_y)]
