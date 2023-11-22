##################################
composite uFJC scission UFL FEniCS
##################################

|build| |pyversions| |pypi| |license| |zenodo|

The Python package for the composite uFJC model with scission implemented in the Unified Form Language (UFL) for FEniCS. This repository is dependent upon the `composite-uFJC-scission <https://pypi.org/project/composite-ufjc-scission/>`_ Python package.

************
Installation
************

This package can be installed using ``pip`` via the `Python Package Index <https://pypi.org/project/composite-ufjc-scission-ufl-fenics/>`_ (PyPI),

::

    pip install composite-ufjc-scission-ufl-fenics

Alternatively, a branch can be directly installed using

::

    pip install git+https://github.com/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS.git@<branch-name>

or after cloning a branch, moving to the main project directory (where the setup and configuration files are located), and executing ``pip install -e .`` for an editable installation or ``pip install .`` for a standard installation.

***********
Information
***********

- `License <https://github.com/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS/LICENSE>`__
- `Releases <https://github.com/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS/releases>`__
- `Repository <https://github.com/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS>`__

********
Citation
********

\Jason Mulderrig, Brandon Talamini, and Nikolaos Bouklas, ``composite-ufjc-scission-ufl-fenics``: the Python package for the composite uFJC model with scission implemented in the Unified Form Language (UFL) in FEniCS, `Zenodo (2023) <https://doi.org/10.5281/zenodo.7738019>`_.

\Jason Mulderrig, Brandon Talamini, and Nikolaos Bouklas, ``composite-ufjc-scission``: the Python package for the composite uFJC model with scission, `Zenodo (2022) <https://doi.org/10.5281/zenodo.7335564>`_.

\Jason Mulderrig, Brandon Talamini, and Nikolaos Bouklas, A statistical mechanics framework for polymer chain scission, based on the concepts of distorted bond potential and asymptotic matching, `Journal of the Mechanics and Physics of Solids 174, 105244 (2023) <https://www.sciencedirect.com/science/article/pii/S0022509623000480>`_.

..
    Badges ========================================================================

.. |build| image:: https://img.shields.io/github/checks-status/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS/main?label=GitHub&logo=github
    :target: https://github.com/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/composite-ufjc-scission-ufl-fenics.svg?logo=python&logoColor=FBE072&color=4B8BBE&label=Python
    :target: https://pypi.org/project/composite-ufjc-scission-ufl-fenics/

.. |pypi| image:: https://img.shields.io/pypi/v/composite-ufjc-scission-ufl-fenics?logo=pypi&logoColor=FBE072&label=PyPI&color=4B8BBE
    :target: https://pypi.org/project/composite-ufjc-scission-ufl-fenics/

.. |license| image:: https://img.shields.io/github/license/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS?label=License
    :target: https://github.com/jasonmulderrig/composite-uFJC-scission-UFL-FEniCS/LICENSE

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7738019.svg
   :target: https://doi.org/10.5281/zenodo.7738019