from setuptools import setup, find_packages

from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='digimat.ebix',
    version='0.0.4',
    description='Digimat EBIX files helper',
    long_description=long_description,
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@st-sa.ch',
    url='https://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['digimat/ebix/data/*.xml']},
    install_requires=[
        'pyyaml',
        'pytz',
        'python-dateutil',
        'requests',
        'prettytable',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False)
