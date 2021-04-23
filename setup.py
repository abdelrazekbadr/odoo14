#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from os.path import join, dirname
import os

exec(open(join(dirname(__file__), 'odoo', 'release.py'), 'rb').read())  # Load release variables
lib_name = 'odoo'

def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for f in files:
            stubs.append(os.path.relpath(os.path.join(root, f), package))
    return {package: stubs}

setup(
    name='odoo',
    version=version,
    description=description,
    long_description=long_desc,
    url=url,
    author=author,
    author_email=author_email,
    classifiers=[c for c in classifiers.split('\n') if c],
    license=license,
    scripts=['setup/odoo'],
    packages=find_packages(),
    package_dir={'%s' % lib_name: 'odoo'},
    include_package_data=True,
    install_requires=[
        'babel >= 1.0',
        'decorator',
        'docutils',
        'feedparser',
        'gevent',
        'html2text',
        'idna',
        'Jinja2',
        'lxml',  # windows binary http://www.lfd.uci.edu/~gohlke/pythonlibs/
        'libsass',
        'mako',
        'mock',
        'ofxparse',
        'passlib',
        'pillow',  # windows binary http://www.lfd.uci.edu/~gohlke/pythonlibs/
        'polib',
        'psutil',  # windows binary code.google.com/p/psutil/downloads/list
        'psycopg2 >= 2.2',
        'pydot',
        'pyparsing',
        'pypdf2',
        'pyserial',
        'python-dateutil',
        'python-stdnum',
        'pytz',
        'pyusb >= 1.0.0b1',
        'qrcode',
        'reportlab',  # windows binary pypi.python.org/pypi/reportlab
        'requests',
        'zeep',
        'vobject',
        'werkzeug',
        'xlsxwriter',
        'xlwt',
    ],
    python_requires='>=3.6',
    extras_require={
        'ldap': ['python-ldap'],
        'SSL': ['pyopenssl'],
    },
    tests_require=[
        'freezegun',
    ],
)

setup(
    name="odoo14-stubs",
    url="https://github.com/trinhanhngoc/odoo-stubs",
    author="Trinh Anh Ngoc",
    author_email="atw1990@gmail.com",
    version="0.0.1",
    package_data=find_stubs("odoo-stubs"),
    packages=["odoo-stubs"]
)
setup(
    name='pydevd-odoo',
    version='1.1',
    description='PyDev.Debugger plugin for Odoo',
    url='https://github.com/trinhanhngoc/pydevd-odoo',
    author='Trinh Anh Ngoc',
    author_email='atw1990@gmail.com',
    packages=find_packages(),
    namespace_packages=['pydevd_plugins.extensions'],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
