from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

extension = [Extension(name = "calculator.cython_mod",
                       sources = ["calculator/cython_mod.pyx"])
            ]

setup(
    name = "calculator",
    ext_modules=cythonize(extension),
)

