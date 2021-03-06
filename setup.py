import logging
import re
import subprocess
import sys
from distutils.core import Command

from setuptools import find_packages, setup

with open('bynder_sdk/version.py', 'r', encoding='utf-8') as version_file:
    version = re.search(
        r'VERSION = [\'"]([^\'"]+)', version_file.read(), re.MULTILINE
    ).group(1)

with open("README.md", 'r') as readme:
    LONG_DESC = readme.read()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def _run_linters():
    linters = {
        'flake8': ['flake8']
    }

    if sys.version_info >= (3, 5, 3):
        # https://github.com/PyCQA/pylint/issues/1388
        linters.update({'pylint': ['pylint', '--output-format', 'parseable']})

    for linter_name, command in linters.items():
        log.info('Running %s', linter_name)

        if subprocess.call(command + ['bynder_sdk', 'test']):
            raise SystemExit('{} failed'.format(linter_name))


def _run_type_linting():
    if subprocess.call(
            ['mypy',
             '--ignore-missing-imports',
             '--follow-imports=skip',
             'bynder_sdk']):
        raise SystemExit('Type hinting checks failed.')


def _run_tests():
    if subprocess.call(
            ['pytest',
             '--cov-report', 'term-missing:skip-covered',
             '--cov-report', 'xml',
             '--cov', 'bynder_sdk',
             '--cov', 'test',
             'test']):
        raise SystemExit('Linting failed.')


def _run_listdeps():
    regex = re.compile('.*bynder.*')
    bynder_deps = filter(regex.match, requires)
    print(' '.join(bynder_deps))


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        subprocess.call(['pip', 'install'] + requires + test_requires)

    def finalize_options(self):
        pass

    def run(self):
        _run_tests()


class Linting(Command):
    user_options = []

    def initialize_options(self):
        subprocess.call(['pip', 'install'] + requires + test_requires)

    def finalize_options(self):
        pass

    def run(self):
        _run_linters()
        _run_type_linting()


class ListDeps(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        _run_listdeps()


class TestDeps(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(' '.join(test_requires))


requires = [
        'requests>=2.20.0,<=3.0.0',
        'requests_oauthlib>=1.1.0,<=2.0.0',
]

test_requires = [
    'pylint',
    'mypy',
    'pytest',
    'pytest-cov',
    'flake8',
]

commands = {
    'test': PyTest,
    'lint': Linting,
    'listdeps': ListDeps,
    'testdeps': TestDeps,
}

setup(
    name='bynder-sdk',
    version=version,
    description=(
        'Bynder SDK can be used to speed up the'
        ' integration of Bynder in Python'
    ),
    long_description=LONG_DESC,
    long_description_content_type='text/markdown',
    url='https://bynder.com',
    author='Bynder',
    author_email='techteam@bynder.com',
    license='MIT',
    cmdclass=commands,
    packages=find_packages(),
    install_requires=requires,
    tests_require=test_requires,
    include_package_data=True,
    keywords='bynder, dam',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    zip_safe=False
)
