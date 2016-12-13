from setuptools import setup, find_packages
import os
import glob

setup(
    name = 'lightcurve',
    url = 'http://justincely.github.io/lightcurve/',
    version = '0.5.2',
    description = 'Create lightcurves from HST/COS data',
    author = 'Justin Ely',
    author_email = 'ely@stsci.edu',
    keywords = ['astronomy'],
    classifiers = ['Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Development Status :: 1 - Planning',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
    packages = find_packages(),
    install_requires = ['astropy',
                        'scipy',
                        'numpy>=1.9',
                        'numba>=0.24.0'],
    scripts =  ['scripts/lightcurve'],
    )
