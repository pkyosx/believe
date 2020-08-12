import os

from setuptools import find_packages, setup

try:
    version = os.environ['VERSION']
except:
    version = '1.0.4'

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, '../', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name='believe',
        version=version,
        description='A easy to use validator for json content',
        long_description=long_description,
        long_description_content_type='text/markdown',
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
