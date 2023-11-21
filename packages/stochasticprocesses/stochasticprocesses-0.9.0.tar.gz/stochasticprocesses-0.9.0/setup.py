from setuptools import setup, find_packages

with open("Readme.md", "r") as f:
    long_description = f.read()
    
setup (
    author= "Julio César Martínez",
    description="A package to simulate stochastic proccesses",
    long_description = long_description,
    long_description_content_type="text/markdown",
    name='stochasticprocesses',
    version='0.9.0',
    packages=find_packages(include=["numpy", "pandas"]),
    author_email="julio.martinez@gmail.com.mx",
    install_requires=["pandas >= 1.0.0", "numpy >= 1.15.0"],
    python_requires=">= 3.7.3",
    url='https://github.com/JulioCesarMS/StochasticModels.git'
    ),


# pip install -e .
