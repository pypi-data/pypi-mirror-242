#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    extensions = []
else:
    extensions = cythonize([
        Extension(
            "pytoshop.packbits",
            ["pytoshop/packbits.pyx"]
        )
    ])

# This function will be executed in setup.py:
def build(setup_kwargs):
    # Build
    setup_kwargs.update({
        'ext_modules': extensions,
    })
