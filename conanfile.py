# conanfile.py - Recipe file for conan build
# copyright Aptera Motors 2021

from conans import ConanFile, tools
import os

class BuildLibNlohmannJsonConan(ConanFile):
    name = "libnlohmann-json"
    settings = "os", "compiler", "build_type", "arch"
    license = "MIT"
    no_copy_source = True
    version="3.9.1"

    def source(self):
        githubVersion = "v" + self.version       # this repo uses a "v" prefix on version numbers on github
        print("Fetching", githubVersion, "source from github\n")
        git = tools.Git(folder="json")
        git.clone("https://github.com/nlohmann/json.git", shallow=True)

        # fetch tag from remote repo
        fetchString = 'git --git-dir=json/.git fetch origin refs/tags/' + githubVersion + ":refs/tags/" + githubVersion
        os.system(fetchString)

        # switch to tag
        git.checkout(githubVersion)

    def package(self):
        self.copy("include/*", src="json/", keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ["include"]

    def package_id(self):
        # prevent extra unneeded copy of source into build folder (keeps conan repo smaller)
        self.info.header_only()
