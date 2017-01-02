#CK note: to be changed as code progresses
from setuptools import setup #,find_packages
#from codecs import open
#from os import path

#here = path.abspath(path.dirname(__file__))

#with open(path.join(here,'docs/README.txt'), encoding = 'utf-8') as f:
#    long_description = f.read()

#From: https://docs.python.org/2/distutils/setupscript.html
# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(
    name='ExoplanetSpectra',
    version='0.1',
    description='Extract exoplanet transmission spectra from multi-wavelength light curves',
    #long_description = long_description,
    url = 'https://github.com/ckreisch/ExoplanetSpectra',
    author = 'Brianna Lacy, Christina Kreisch, Heather Prince, Polina Kanel, Julien de Lanversin, Blake Yang',
    author_email = 'blacy@princeton.edu',
    license='GNU GENERAL PUBLIC LICENSE', #should we change? is this line redundant?
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Astronomy'
        ],
    #keywords = 'Convex Optimization SDP',
    #test_suite =  'nose.collector',
    #tests_require = ['nose'],
    #packages=find_packages(exclude = ['contrib','docs','tests*']), #TO SET LATER
    #scripts=['bin/points.py','bin/alignment.py'],
    install_requires=[
                    'numpy',
                    'scipy',
                    'matplotlib',
                    'os',
                    'math',
                    'time',
                    'read_input',
                    're',
                    'ast',
                    'itertools',
                    'decimal',
                    'pylab',
                    'unittest',
                    'glob',
                    'mpi4py',
                    'emcee',
                    'george',
                    'batman',
                    'corner'
                    ]
    #move some of above into extras_requires ?


)
