import os
from setuptools import setup

setup(
    name='trfind',
    version='0.0.5',
    author='Jason Curtis and Jaime McCandless',
    description='Finds trip reports from the Internet',
    url='http://github.com/thatneat/trfind',
    packages=['trfind'],
    install_requires=[
        'beautifulsoup',
        'Flask',
        'Flask-Cors',
        'lxml',
        'mechanize',
        'petl',
        'python-dateutil',
        'requests',
    ],
    entry_points={
        'console_scripts': ['trfind = trfind.find:main']
    },
    include_package_data=True
)
