import distutils
import os

from setuptools import setup
from setuptools.command.install import install

from pathlib import Path
from setuptools import setup, find_packages 

current_dir = Path(__file__).parent.resolve()

with open(current_dir / "README.md", encoding="utf-8") as f:
    long_description = f.read()

class Installer(install):
    def initialize_options(self):
        super().initialize_options()
        contents = "import sys; exec({!r})\n".format(self.read_pth("tiefighter.pth"))
        self.extra_path = (self.distribution.metadata.name, contents)

    def read_pth(self, path):
        with open(path) as f:
            content = f.read()
        return content

    def finalize_options(self):
        super().finalize_options()

        install_suffix = os.path.relpath(self.install_lib, self.install_libbase)
        if install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase


setup(
    name="tiefighter",
    version="1.0.0",
    description="Tiefighter operator",
    author = "btaskaya",
    author_email = "batuhanosmantaskaya@gmail.com",
    url = "https://github.com/isidentical/tiefighter",
    py_modules=["tiefighter"],
    cmdclass={"install": Installer},
    long_description = long_description,
    long_description_content_type = "text/markdown",

)
