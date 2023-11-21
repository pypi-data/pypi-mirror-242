from setuptools import setup, find_packages

with open("Readme.md", "r") as f:
    long_description = f.read()
    
setup (
    author= "Julio César Martínez",
    description="A package to simulate stochastic proccesses",
    long_description = long_description,
    long_description_content_type="text/markdown",
    name='StochasticProcesses',
    version='0.6.0',
    packages=find_packages(include=["numpy", "pandas"]),
    author_email="julio.martinez@gmail.com.mx",
    install_requires=["pandas >= 1.5.3", "numpy >= 1.23.5"],
    python_requires=">= 3.9.4",
    url='https://github.com/JulioCesarMS/StochasticModels.git'
    ),


# pip install -e .