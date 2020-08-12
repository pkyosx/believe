import os

from setuptools import find_packages, setup

try:
    version = os.environ['VERSION']
except:
    version = '1.0.1'

if __name__ == '__main__':
    setup(
        name='believe',
        version=version,
        description='A easy to use validator for json content',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        python_requires='>=3.0',
        keywords=['json', 'validate', 'validator'],
        author='Seth Wang',
        author_email='pkyosx@gmail.com',
        url='https://github.com/pkyosx/believe',
        packages=find_packages(exclude=["ez_setup", "examples", "*.tests", "*.tests.*", "tests.*", "tests"]),
        include_package_data=True,
    )
