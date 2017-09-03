#!/usr/bin/python3

from distutils.core import setup

setup(
    name='linux-desktop-manager',
    version='0.1',
    description='Remote manager for Linux desktops',
    author='Omer Akram',
    author_email='om26er@gmail.com',
    packages=['ldm', 'wamp'],
    entry_points={
        'console_scripts': ['linux-desktop-manager = wamp.display_component:main']
    },
)
