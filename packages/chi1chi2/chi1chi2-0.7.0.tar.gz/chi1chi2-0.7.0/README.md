# *chi1chi2* program

The aim of the program is to calculate linear (refractive indices) 
and nonlinear (*chi(2)* for second harmonic generation) 
optical properties of organic crystals.

[TOC]

---

## Installation

**The easiest path** with *conda*:

```
conda create --name chi1chi2 python=3.7 -y
conda activate chi1chi2
conda install -c tomeks86 chi1chi2
```

**The easy path** with docker image:

```
workdir=$(pwd) # or any other directory of your choice
docker run -v $(workdir):/chi1chi2 -it tomeks86/python-chi1chi2 bash
```

**The hard path**

*Warning*: manual installation and getting the program to its full functionality
requires quite much of expertise even in linux (I do not give any warranty that it is
possible to run it in any other OS) and can be a very daunting task.

Make sure you have installed:
 - gfortran
 - python 3.6
 - open babel

Installation:
 - pip install chi1chi2
 - for the fortran programs a Makefile is provided with the repository:
   *make* command builds the programs in the build/ directory

**Easier installation of openbabel using conda**

- *conda env create --file=chi1chi2.yaml*
- for program usage activate the environment with: *conda activate chi1chi2*
- follow the installation of other dependencies with *pip*

#Description

The whole program constitutes a set of scripts that need to be executed in order.

There are four main steps:

1. Input preparation (optionally - geometry optimization)
2. Optical properties of molecular sub-units calculations
3. Calculations of bulk properties
4. Analysis of the results

The purpose of this file is to lead the user through all these steps.


Step *1* - Input preparation
____________________________

A) from Cif (easy path)

use *chi.from_cif* to get geometry for further optimization with *e.g.* crystal09/14/..

B) from fractional coordinates

use *chi.from_fra* script (see: examples/mna_cif.fra, examples/mna_cif2.fra to see the convention)
(remember to adjust the symmetry operations!)

C) manually

see examples for the convention


Step *1a* after geometry optimization
_____________________________________

D) use *chi.from_crystal* script to adjust the coordinates and charges after *crystal* geometry optimization

E) run *chi.input_preparator* script to get input files for:

- *charge_generator* program (example usage: *charge_generator < chg1.inp*)
- Lorentz tensor with *lorentz* program (example usage: *lorentz < lorentz.inp > L.dat*)


Step *2* - property calculation
_______________________________

Use sets of charges, geometries and follow your favorite property calculation procedure.
Additional shell scripts could be provided in later releases.

Step *3* - core calculations
____________________________

Use the script *chi.main* to get the `chi(1)` and `chi(2)` tensor components in the so called a'bc* reference frame.

Q-LFT calculations enabled! (since 0.1.1)

Step *4* - result analysis
__________________________

Use the script *chi.analyze* with output file generated in step 3

- Refractive indices analysis (since 0.1.3)
- Magnitude of the `chi(2)` tensor components in the direction of the optical indicatrix (since 0.1.3)


Helpers
-------

Helper scripts are available to use around molecular calculations:
 - *read_g09.py* for reading the molecular properties after the QC calculations
 - *scale_props.py* for scaling the static properties with use of the reference calculations
 - *calc_pol.py* for calculation of distributed polarizabilities using AIMALL output of finite field calculations

Note: the scripts minimize depencencies on the project library so that they could
be used as standalone scripts on an external machine

Preparations for distributed polarizabilities calculations
----------------------------------------------------------

Two variants are possible:
 - with only one external field magnitude (0.003 a.u.)

  The input files for AIMALL have to be preparated in the following convention:

  1 /no field/; 2 /0.003, 0, 0/; 3 /0, 0.003, 0/; 4 /0, 0, 0.003/;

  5 /-0.003, 0, 0/; 6 /0, -0.003, 0/; 7 /0, 0, -0.003/

 - with two external field magnitudes (0.003 a.u. and 0.006 a.u.)
   (using Romberg numerical differentiation procedure)

  The input files for AIMALL should follow the convention:

  1 /no field/; 2 /0.003, 0, 0/; 3 /0, 0.003, 0/; 4 /0, 0, 0.003/;

  5 /-0.003, 0, 0/; 6 /0, -0.003, 0/; 7 /0, 0, -0.003/

  8 /0.006, 0, 0/; 9 /0, 0.006, 0/; 10 /0, 0, 0.006/;

  11 /-0.006, 0, 0/; 12 /0, -0.006, 0/; 13 /0, 0, -0.006/

Examples
--------

See the examples/examples.pdf to follow the steps used in the integration tests.
The files used for the tests are located in the tests/integration directory:

- *input* as a starting point
- *expected* as a reference

Example gaussian09 input file for calculations could be found in examples/mna.com

Version history
---------------

- 0.1.0 - first release (31.01.2019)
- 0.1.1 - Q-LFT calculations support added (05.02.2019)
- 0.1.2 - a minor README fix on the PyPI (06.02.2019)
- 0.2.0 - analysis of the core calculations - reporting in tables (09.03.2019)
- 0.2.1 - property scaling helper (27.03.2019)
- 0.3.0 - atomic polarizability scaling approach change (03.03.2020)
- 0.4.0 - distributed polarizability calculation script & format change (10.03.2020)
- 0.4.1 - correction of molecules placement in the unit cell (23.03.2020)
- 0.5.0 - from_crystal old input backing up strategy change (04.04.2020)
- 0.5.1 - HYDROGEN_TOLERANCE environment variable could be used to modify default maximum hydrogen distance (1.15A)
- 0.6.1 - input preparation and main calculations allow for arbitrary redefinition 
of molecule-ionic composition of the unit cell (31.08.2020)
- 0.7.0 - fix for calculation of properties in non-orthogonal systems (15.02.2021)
