# -*- coding: utf-8 -*-

from __future__ import absolute_import

import codecs

from setuptools import setup

setup(
    name='ssd_checker',
    version=open('VERSION').read().strip(),
    description='Solid-state drive (ssd) checker',
    long_description=codecs.open(
        'README.rst', encoding='utf-8', errors='ignore').read(),
    keywords='ssd check checker solid state drive pyssd',
    url='https://github.com/kipodd/ssd_checker',
    download_url='https://github.com/kipodd/ssd_checker/releases',
    author='kipodd',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities'],
    platforms=['any'],
    py_modules=['ssd_checker'],
    include_package_data=True,
    install_requires=[
        'psutil;os_name!="nt"',
        'pypiwin32>=154;os_name=="nt"',
        'wmi;os_name=="nt"'],
    setup_requires=['setuptools>=20.8.1'],
    python_requires='>=2.6,!=3.0,!=3.1,!=3.2',
    zip_safe=True)
