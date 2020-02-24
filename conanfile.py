from conans import ConanFile, CMake, tools
import os

class KeychainConan(ConanFile):
    name = "keychain"
    description = "A cross-platform wrapper for the operating system's credential storage"
    topics = ("conan", "security", "keychain")
    url = "https://github.com/reneme/conan-keychain"
    homepage = "https://github.com/hrantzsch/keychain"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def requirements(self):
        # Note: keychain requires 'libsecret-1' on Linux which is not in Conan. libsecret must
        # therefore be installed on the system manually.
        # It further requires `glib-2.0` (via libsecret), which is in Conan. However, we cannot use
        # it as it might be incompatible with the system-installed version of libsecret.
        # For both of these dependencies, keychain relies on pkgconfig in order to find them. Once
        # both of the dependencies are available in Conan, we can use `pkg-config_installer` to find
        # them via pkgconfig.
        #
        # check if pkgconfig can find the dependencies
        tools.PkgConfig("libsecret-1")
        tools.PkgConfig("glib-2.0")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

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
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["secret-1", "glib-2.0"]
