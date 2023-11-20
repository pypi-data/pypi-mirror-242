from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
        name="HEtools", 
        version="0.4.0",
        author="Bastiaan Quast",
        author_email="<bquast@gmail.com>",
        packages=find_packages(),
        install_requires=['numpy',],
        long_description=long_description,
        long_description_content_type='text/markdown',
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
