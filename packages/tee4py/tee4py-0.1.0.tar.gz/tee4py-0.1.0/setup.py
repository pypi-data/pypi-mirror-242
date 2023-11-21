from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

exec(open('tee4py/_version.py').read()) # get version number

setup(
    name='tee4py',
    version=__version__,
    author='Rhydian Lewis',
    author_email='rhydian.lewis@swansea.ac.uk',
    description='tee4py is a python implementation the Unix tee command, allowing output to be written to the terminal and a file simultaneously.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/RhydianL/python_tee',    
    packages=['tee4py'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)