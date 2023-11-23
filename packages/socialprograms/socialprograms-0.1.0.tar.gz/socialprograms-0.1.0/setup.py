from setuptools import setup, find_packages
import io
import os


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

setup(
    name='socialprograms',
    description='A package to evaluate social programs',
    author='dgria-inteligencia',
    author_email='sesna.dgria.inteligencia@gmail.com',
    version='0.1.0',
    long_description=read('Readme.md'),
    long_description_content_type='text/markdown',
    #packages=['socialprograms'],
    packages=find_packages(),
    install_requires=["pandas >= 1.0.0", "numpy >= 1.15.0"],
    python_requires=">= 3.11.0",
    url='https://github.com/SESNA-Inteligencia/Algoritmos',
    

)

# pip install -e .
