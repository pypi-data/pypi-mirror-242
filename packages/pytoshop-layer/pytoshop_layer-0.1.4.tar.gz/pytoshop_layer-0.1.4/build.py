#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

from distutils.core import Distribution, Extension
from Cython.Build import cythonize, build_ext
extensions = cythonize([
    Extension(
        "pytoshop.packbits",
        ["pytoshop/packbits.pyx"]
    )
])
dist = Distribution({"ext_modules": extensions})
cmd = build_ext(dist)
cmd.ensure_finalized()
cmd.run()

for output in cmd.get_outputs():
    relative_extension = os.path.relpath(output, cmd.build_lib)
    shutil.copyfile(output, relative_extension)
