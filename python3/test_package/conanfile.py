import os

from conans import ConanFile, CMake, tools


class PythonTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "make"

    def build(self):
        return
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        return
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        return
        if not tools.cross_building(self.settings):
            os.chdir("bin")
