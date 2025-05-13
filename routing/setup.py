from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "astarCython",
        ["astarC.pyx"],
        include_dirs=[np.get_include()],
        define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
    )
]

setup(
    name="astarC",
    ext_modules=cythonize(
        extensions,
        annotate=True,
        compiler_directives={'language_level': "3"}
    ),
    zip_safe=False,
)

# python setup.py build_ext --inplace