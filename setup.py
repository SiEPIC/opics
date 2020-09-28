#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]


with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = ['Click>=7.0', ]+parse_requirements('requirements.txt')

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jaspreet Jhoja",
    author_email='jaspreet@siepic.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Open-source frequency domain solver for photonic integrated circuits.",
    entry_points={
        'console_scripts': [
            'opics=opics.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='opics',
    name='opics',
    packages=find_packages(include=['opics', 'opics.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/siepic/opics',
    version='0.2.0',
    zip_safe=False,
)
