from setuptools import find_packages, setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='sphinxcontrib-opencontracting',
    version='0.0.1',
    author='Open Contracting Partnership',
    author_email='data@open-contracting.org',
    url='https://github.com/open-contracting/sphinxcontrib-opencontracting',
    description='Provides Sphinx directives for the documentation of the Open Contracting Data Standard',
    license='BSD',
    packages=find_packages(exclude=['tests', 'tests.*']),
    namespace_packages=['sphinxcontrib'],
    long_description=long_description,
    install_requires=[
        'commonmark',
        'docutils',
        'jsonpointer',
        'MyST-Parser',
        'requests',
        'ocdsextensionregistry>=0.0.8',
    ],
    extras_require={
        'test': [
            'coveralls',
            'lxml',
            'pytest',
            'pytest-cov',
            'Sphinx',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
