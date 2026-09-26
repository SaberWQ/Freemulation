from setuptools import setup
from Cython.Build import cythonize

setup(
    name='fast_analyzer',
    ext_modules=cythonize("fast_core/fast_analyzer.pyx"),
)