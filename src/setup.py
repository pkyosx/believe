import os

from setuptools import find_packages, setup

try:
    version = os.environ['VERSION']
except:
    version = '1.0.0'

if __name__ == '__main__':
    setup(
        name='believe',
        version=version,
        description='A easy to use validator for json content',
        classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        keywords=['json', 'validate', 'validator'],
        author='Seth Wang',
        author_email='pkyosx@gmail.com',
        url='https://github.com/pkyosx/believe',
        packages=find_packages(exclude=["ez_setup", "examples", "*.tests", "*.tests.*", "tests.*", "tests"]),
        include_package_data=True,
    )
