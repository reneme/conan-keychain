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

    def build_requirements(self):
        if self.settings.os == "Linux":
            self.build_requires("pkg-config_installer/0.29.2@bincrafters/stable")

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("glib/2.58.3@bincrafters/stable")
            # TODO: keychain also requires 'libsecret-1' which is not in conan

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
