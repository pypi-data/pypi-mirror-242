from setuptools import setup, find_packages
import io
import os


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

setup(
    name='stochasticprocesses',
    description='A package to simulate stochastic processes',
    author='Julio César Martínez',
    author_email='julio.martinez@gmail.com.mx',
    version='0.14.0',
    long_description=read('Readme.md'),
    long_description_content_type='text/markdown',
    #packages=['simulation'],
    packages=find_packages(include=["numpy", "pandas", "random"]),
    install_requires=["pandas >= 1.0.0", "numpy >= 1.15.0"],
    python_requires=">= 3.7.3",
    url='https://github.com/JulioCesarMS/StochasticModels.git',
    

)

# pip install -e .
