#!/usr/bin/env python

# Copyright 2009 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.restful
#
# lazr.restful is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.restful is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.restful.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

# generic helpers primarily for the long_description
def generate(*docname_or_string):
    res = []
    for value in docname_or_string:
        if value.endswith('.rst'):
            f = open(value)
            value = f.read().split('..\n    end-pypi', 1)[0]
            f.close()
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers

__version__ = open("src/lazr/restful/version.txt").read().strip()

setup(
    name='lazr.restful',
    version=__version__,
    namespace_packages=['lazr'],
    packages=find_packages('src'),
    package_dir={'':'src'},
    include_package_data=True,
    zip_safe=False,
    maintainer='LAZR Developers',
    maintainer_email='lazr-developers@lists.launchpad.net',
    description=open('README.rst').readline().strip(),
    long_description=generate(
        'src/lazr/restful/docs/index.rst',
        'NEWS.rst'),
    license='LGPL v3',
    install_requires=[
        'docutils>=0.3.9',
        'grokcore.component>=1.6',
        'lazr.batchnavigator>=1.2.0-dev',
        'lazr.delegates>=2.0.3',
        'lazr.enum',
        'lazr.lifecycle',
        'lazr.uri',
        'martian>=0.11',
        'pytz',
        'setuptools',
        'simplejson>=2.1.0',
        'six>=1.13.0',
        'testtools',
        'van.testing',
        'wsgiref; python_version < "3"',
        'zope.component [zcml]',
        'zope.configuration',
        'zope.datetime',
        'zope.event',
        'zope.interface>=3.8.0',
        'zope.pagetemplate',
        'zope.processlifetime',
        'zope.proxy',
        'zope.publisher; python_version < "3"',
        'zope.publisher>=6.0.0; python_version >= "3"',
        'zope.schema',
        'zope.security',
        'zope.traversing',
        ],
    url='https://launchpad.net/lazr.restful',
    download_url= 'https://launchpad.net/lazr.restful/+download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        ],
    extras_require=dict(
        docs=['Sphinx'],
        test=['zope.testing>=4.6.0'],
        xml=['lxml',] # requiring this of normal users is too much
    ),
    test_suite='lazr.restful.tests',
    )
