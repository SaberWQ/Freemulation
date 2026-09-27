from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="fast_core.browser",
        sources=["fast_core/browser.pyx", "fast_core/browser_engine.cpp"],
        language="c++",
        extra_compile_args=["-O3", "-std=c++17"], # Оптимізація швидкості
    )
]

setup(
    ext_modules=cythonize(extensions)
)