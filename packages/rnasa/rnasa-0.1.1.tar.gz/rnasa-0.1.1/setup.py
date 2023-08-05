#!/usr/bin/env python

from setuptools import find_packages, setup

from rnasa import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='rnasa',
    version=__version__,
    author='Daichi Narushima',
    author_email='dnarsil+github@gmail.com',
    description='Gene Expression Level Calculator for RNA-seq',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dceoy/rnasa',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['docopt', 'ftarc', 'luigi', 'pandas', 'psutil'],
    entry_points={
        'console_scripts': ['rnasa=rnasa.cli.main:main']
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    python_requires='>=3.6',
)
