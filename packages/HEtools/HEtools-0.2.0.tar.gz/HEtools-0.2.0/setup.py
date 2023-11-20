from setuptools import setup, find_packages

setup(
        name="HEtools", 
        version="0.2.0",
        author="Bastiaan Quast",
        author_email="<bquast@gmail.com>",
        packages=find_packages(),
        install_requires=['numpy',],
        keywords=['homomorphic encryption', 'FHE', 'cryptography', 'coefmod', 'modulo', 'coefficient modulo', 'polynomial'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
