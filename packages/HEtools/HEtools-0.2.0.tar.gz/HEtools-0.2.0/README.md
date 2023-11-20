# HEtools

[![License](https://img.shields.io/badge/license-GPLv3-brightgreen.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![Verson](https://img.shields.io/pypi/v/HEtools.svg)](https://pypi.org/project/HEtools/)


Homomorphic encryption (Brakerski and Vaikuntanathan (2014) <doi:10.1137/120868669>) using Ring Learning with Errors (Lyubashevsky et al. (2012) <https://eprint.iacr.org/2012/230>) is a form of Learning with Errors (Regev (2005) <doi:10.1145/1060590.1060603>) using polynomial rings over finite fields. Functions to generate the required polynomials (using 'polynom'), with various distributions of coefficients are provided. Additionally, functions to generate and take coefficient modulo are provided.

## Installation

You can install HEtools using

```
pip install HEtools
```


## Example

This is a basic example which shows you how to solve a common problem:

``` python
import HEtools
from numpy.polynomial import Polynomial

p = Polynomial((9,8,13))
coefmod(p,2)
```
