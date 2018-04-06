#!/usr/bin/python3

from distutils.core import setup

setup(
    name='linux-desktop-manager',
    version='0.2',
    description='Remote manager for Linux desktops',
    author='Omer Akram',
    author_email='om26er@gmail.com',
    packages=['linux_desktop_manager', 'linux_desktop_manager.wamp', 'linux_desktop_manager.controller'],
    entry_points={
        'console_scripts': ['linux-desktop-manager = linux_desktop_manager.wamp.display_component:main']
    }
)
