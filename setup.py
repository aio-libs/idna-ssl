import io
import os
import re
import sys

from setuptools import setup

needs_pytest = 'pytest' in set(sys.argv)


def get_version():
    regex = r"__version__\s=\s\'(?P<version>[\d\.]+?)\'"

    path = ('idna_ssl.py',)

    return re.search(regex, read(*path)).group('version')


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


setup(
    name='idna_ssl',
    version=get_version(),
    author='OCEAN S.A.',
    author_email='osf@ocean.io',
    url='https://github.com/wikibusiness/idna_ssl',
    description='Patch ssl.match_hostname for Unicode(idna) domains support',
    long_description=read('README.rst'),
    setup_requires=['pytest-runner'] if needs_pytest else [],
    tests_require=['pytest', 'pytest-asyncio', 'pytest-cov', 'aiohttp>2.3'],
    py_modules=['idna_ssl'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['ssl', 'Unicode', 'idna', 'match_hostname'],
)
