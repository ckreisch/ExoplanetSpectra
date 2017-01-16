# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

# From: https://docs.python.org/2/distutils/setupscript.html
# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(
    name='ExoSpec',
    version='0.1',
    description='Extract exoplanet transmission spectra from multi-wavelength light curves',
    #long_description = long_description,
    url = 'https://github.com/ckreisch/ExoplanetSpectra',
    author = 'Brianna Lacy, Christina Kreisch, Heather Prince, Polina Kanel, Julien de Lanversin, Blake Yang',
    author_email = 'blacy@princeton.edu',
    license='GNU GENERAL PUBLIC LICENSE',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Unix',
#        'Programming Language :: Python :: 2',
#        'Programming Language :: Python :: 2.3',
#        'Programming Language :: Python :: 2.4',
#        'Programming Language :: Python :: 2.5',
#        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy'
        ],
    keywords = 'Exoplanet spectrum fitter',
    test_suite =  'nose.collector',
    tests_require = ['nose'],
    packages=find_packages(exclude = ['contrib','docs','tests*']),
    scripts=['bin/exospec_main.py','bin/lc_class_demo.py'],
    install_requires=['numpy',
                    'scipy',
                    'matplotlib',
                    'virtualenv',
                    'mpi4py',
                    'emcee',
                    'george',
                    'batman-package',
                    'corner',
                    'pandas']
)
