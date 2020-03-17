#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import setuptools

current_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(current_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

name = "xcomcan"
version = "0.9"
release = "0.9.1"

setuptools.setup(
    name=name,
    version=release,
    author="Studer Innotec SA",
    author_email="develop@studer-innotec.com",
    maintainer_email="develop@studer-innotec.com",
    description="Package that let easily interact with the Xcom-CAN device",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/studer-innotec/xcomcan",
    project_urls={
        "Documentation": "https://xcomcan.readthedocs.io/en/latest/index.html",
        "Issues tracker": "https://github.com/studer-innotec/xcomcan/issues",
        "Source Code": "https://github.com/studer-innotec/xcomcan",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6.8',
    install_requires=['stucancommon>=0.9.1'],
    # these are optional and override conf.py settings
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
            'all_files': ('setup.py', 1)},
    },
)
