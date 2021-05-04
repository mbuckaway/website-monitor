#!/usr/bin/env python3

from setuptools import setup

setup(name='website-monitor',
        version='1.0',
        description='Simple Website Monitor',
        author='Mark Buckaway',
        author_email='mark@buckaway.ca',
        url='https://github.com/website-monitor',
        include_package_data=True,
        packages=['webmonlib'],
        entry_points = {'console_scripts': [
            'webmoncheck = webmonlib.cli_webmoncheck:main', 
            'webmonsave = webmonlib.cli_webmonsave:main', 
            ]},
        install_requires=[
            'wheel',
            'kafka-python',
            'requests',
            'jsonpickle',
            'python-dotenv'
        ]
)