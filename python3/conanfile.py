from conans import AutoToolsBuildEnvironment, ConanFile, tools


class PythonConan(ConanFile):
    name = "Python"
    version = "3.8.0"
    license = "MIT"
    author = "Martyn Gigg <martyn.gigg@gmail.com>"
    description = "Official interpreter of Python language"
    topics = ("cpython",)
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    generators = "make"
    build_requires = "zlib/1.2.11@conan/stable", "OpenSSL/1.1.1c@conan/stable"

    def source(self):
        source_url = "https://www.python.org/ftp/python/"
        tools.get(source_url + "{version}/Python-{version}.tar.xz".format(version=self.version))

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        flags = [
            "--enable-shared",
            "--enable-ipv6",
            "--enable-loadable-sqlite-extensions",
            "--with-dbmliborder=bdb:gdbm",
            "--with-computed-gotos",
            "--without-ensurepip",
            "--with-openssl={}".format(self.deps_cpp_info["OpenSSL"].rootpath)
        ]
        autotools.configure(configure_dir="Python-{}".format(self.version),
                            args=flags)
        autotools.make()

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.make(target='install')

    def package_info(self):
        # TODO: What should be provided here?
        pass
