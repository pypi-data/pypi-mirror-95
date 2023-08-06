from setuptools import setup
from setuptools.command.install import install
import platform, sys, os
from os import path, environ

#------------------------------------
# Start menu item creation on Windows
#------------------------------------

def create_shortcut_under(root, exepath, nulfile):
    import subprocess
    profile = environ[root]
    s = "$s=(New-Object -COM WScript.Shell).CreateShortcut('" + profile + "\\Microsoft\\Windows\\Start Menu\\Programs\\DWARF Explorer.lnk');"
    s += "$s.TargetPath='" + exepath + "';$s.Save()"
    return subprocess.call(['powershell', s], stdout = nulfile, stderr = nulfile) == 0

def create_shortcut():
    try:
        exepath = path.join(path.dirname(sys.executable), "Scripts", "dwex.exe")
        with open(os.devnull, 'w') as nulfile:
            if not create_shortcut_under('ALLUSERSPROFILE', exepath, nulfile):
                create_shortcut_under('APPDATA', exepath, nulfile)
    except:
        pass

#--------------------------------------    

class my_install(install):
    def run(self):
        install.run(self)
        if platform.system() == 'Windows':
            create_shortcut()

# Pull the long desc from the readme
try:
    with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
        long_desc = f.read()          
except:
    long_desc = "GUI viewer for DWARF debug information"

setup(
    name='dwex',
    version='1.11',  # Sync with version in __main__
    packages=['dwex'],
    url="https://github.com/sevaa/dwex/",
    entry_points={"gui_scripts": ["dwex = dwex.__main__:main"]},
    cmdclass={'install': my_install},
    keywords = ['dwarf', 'debug', 'debugging', 'symbols', 'viewer', 'view', 'browser', 'browse', 'tree'],
    license="BSD",
    author="Seva Alekseyev",
    author_email="sevaa@sprynet.com",
    description="GUI viewer for DWARF debug information",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    python_requires=">=3.5",
    setup_requires=[],
    install_requires=['PyQt5', 'filebytes>=0.10.1', 'pyelftools>=0.27'],
    platforms='any',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Environment :: MacOS X :: Cocoa",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Debuggers"
    ]
)

