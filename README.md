# ExoSpec

Welcome to ExoSpec version 0.1, a simple parallelized python 
tool for extracting exoplanet transmission spectra from 
noisey multi-wavelength light curves.
authors: Brianna Lacy, Christina Kreisch, Heather Prince, 
Polina Kanel, Julien de Lanversin, Blake Yang
url: https://github.com/ckreisch/ExoplanetSpectra
email: blacy@princeton.edu

Required Contents:
```
    docs/ 
    bin/ 
    exospec/
    setup.py
    LICENSE.txt     
    README               
```

Within exospec: 
```
    tests/
    out/  
    __init__.py   
    TransitModel.py     
    lc_class.py     
    read_input.py
    mcmc.py         
    read_input_demo.py
    deliverables.py     
    fitting_single_lc.py  
    ```

Within bin:
```
    exospec_main.py
    lc_class_demo.py
    short_example_lc/
    full_example_lc/
    short_example.ini
    full_example.ini
    ```

Within docs:
```
    docs.pdf
    UserManual.pdf 
    ```

# Build/ Install
ExoSpec runs with Python 2.7. 

#Pre-Requisites
Before installing ExoSpec, you must install the following packages:

-Eigen3- 

On linux: 
```
$ sudo apt-get install libeigen3-dev
```
On mac: 
```
$ brew install eigen
```
On Windows: the developers of george say they did not test george on Windows, so it may not work but you can still try. We have not tested ExoSpec on Windows

-OpenMPI-

On linux: 
```
$ sudo apt-get install openmpi-bin openmpi-common openssh-client openssh-server libopenmpi1.3 libopenmpi-dbg libopenmpi-dev
```
On mac: 
```
$ brew install openmpi
```

#Installation

To install ExoSpec run
```
$ python setup.py install
```

Batman issues: If after running the setup.py file you receive and error from batman, you can install it from the source file instead. Download the stable release at https://pypi.python.org/pypi/batman-package/, and then run 
```
$ sudo python setup.py install
```
in the batman directory.

# Tests

To test that the code built correctly, cd to the tests folder and run the tests.py file:
```
$ cd exospec/tests
$ python tests.py
```

# Usage
To run exospec on the two example files included, go into bin/
and simply run:
```
$ python exospec_main.py short_example.ini
$ python exospec_main.py full_example.ini
```

Please see the user manual in the docs/ folder for more
detailed instructions on using exospec with other data.

# Known Issues (v0.1)
- Running 
```
$ python setup.py tests
``` 
 does not run the test suite. This needs to be further investigated.
- Running tests.py with Jenkins on adroit throws an MPI error. We are currently working with David Luet to resolve this.
- We need to add further tests to catch user input errors, such as typing nthreads = 4m instead of nthreads = 4. Currently we have the most basic tests set up.

Jenkins current build status: [![Build Status](https://jenkins.princeton.edu/buildStatus/icon?job=ckreisch/ExoplanetSpectra)](https://jenkins.princeton.edu/buildStatus/icon?job=ckreisch/ExoplanetSpectra)
