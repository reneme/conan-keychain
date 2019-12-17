from conans import ConanFile, CMake, tools
import os


class KeychainConan(ConanFile):
    name = "keychain"
    description = "A cross-platform wrapper for the operating system's credential storage"
    topics = ("conan", "security", "keychain")
    # url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/reneme/keychain"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    version = "latest"

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone(self.homepage)
        git.checkout("feature/install")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs     = ['lib']
        self.cpp_info.libs        = tools.collect_libs(self)

        if self.settings.os == 'Macos':
            self.cpp_info.frameworks = ['Security', 'CoreFoundation']
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ['Crypt32']
