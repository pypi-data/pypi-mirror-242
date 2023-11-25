#  _____ _____ _____
# |_    |   __| __  |
# |_| | |__   |    -|
# |_|_|_|_____|__|__|
# MSR Electronics GmbH
# SPDX-License-Identifier: MIT
#

from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.build_py import build_py
from Cython.Build import cythonize
from sys import platform as os_name
from platform import system, machine, architecture
import shutil
import os
import re

def find_version():
    tld = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(tld, 'ft4222', '__init__.py')
    with open(filename) as f:
        text = f.read()
    match = re.search(r"^__version__ = \"(.*)\"$", text, re.MULTILINE)
    if not match:
        raise RuntimeError('cannot find version')
    return match.group(1)

if system() ==  "Linux":
    if machine() == 'x86_64':
        libdir = "linux/build-x86_64"
    elif machine() == 'i386':
        libdir = "linux/build-i386"
    elif machine() == 'armv7l':
        libdir = "linux/build-arm-v7-hf"
    elif machine().startswith("arm"):
        if architecture()[0] == '64bit':
            libdir = "linux/build-arm-v8"
        else:
            libdir = "linux/build-arm-v6-hf"
    elif machine() == 'aarch64':
        libdir = "linux/build-arm-v8"
    else:
        raise Exception("Unsupported machine and or architecture")

    libs = ["ft4222"]
    incdirs = ["linux"]
    libdirs = [libdir]
    rlibdirs = ['$ORIGIN/.']
    libs_to_copy = ["libft4222.so"]
elif system() == "Darwin":
    libdir = "./osx"
    ft4222_dll = "libft4222.dylib"

    libs = ["ft4222"] #, "ftd2xx"]
    incdirs = ["osx"]
    libdirs = [libdir]
    rlibdirs = [] #'$ORIGIN/.']
    libs_to_copy = [ft4222_dll, "libftd2xx.dylib"]
else:
    if architecture()[0] == '64bit':
        libdir = "win/amd64"
        libs = ["LibFT4222-64", "ftd2xx"]
        libs_to_copy = ["LibFT4222-64.dll", "ftd2xx.dll"]
    else:
        libdir = "win/i386"
        libs = ["LibFT4222", "ftd2xx"]
        libs_to_copy = ["LibFT4222.dll", "ftd2xx.dll"]

    incdirs = ["win"]
    libdirs = [libdir]
    rlibdirs = []

class mybuild(build_py):
    def run(self):
        build_py.run(self)
        print("running mybuild")
        for package, src_dir, build_dir, filenames in self.data_files:
            if package == 'ft4222':
                for lib in libs_to_copy:
                    print("copying {} -> {}".format(libdir + "/" + lib, "ft4222/"+ lib))
                    shutil.copyfile(libdir + "/" + lib, build_dir + "/" + lib)
                break


extensions = [
    Extension("ft4222.ft4222", ["ft4222/ft4222.pyx"],
        libraries=libs,
        include_dirs=incdirs,
        library_dirs=libdirs,
        runtime_library_dirs=rlibdirs,
    ),
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ft4222',
    version=find_version(),
    author='Bearsh',
    author_email='me@bearsh.org',
    url='https://gitlab.com/msrelectronics/python-ft4222',
    description='Python wrapper around libFT4222.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'License :: Other/Proprietary License',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Cython',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Communications',
    ],
    keywords='ftdi ft4222',
    packages=['ft4222', 'ft4222.I2CMaster', 'ft4222.GPIO', 'ft4222.SPI', 'ft4222.SPIMaster', 'ft4222.SPISlave'],
    package_data={
        'ft4222': ['py.typed', 'ft4222.pyi', '__init__.pyi'],
        'ft4222.I2CMaster': ['py.typed'],
        'ft4222.GPIO': ['py.typed'],
        'ft4222.SPI': ['py.typed'],
        'ft4222.SPIMaster': ['py.typed'],
        'ft4222.SPISlave': ['py.typed'],
    },
    ext_modules=cythonize(extensions),
    cmdclass={'build_py': mybuild},
)
