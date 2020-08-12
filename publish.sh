pip install setuptools wheel twine
pushd src
rm -rf dist/
python setup.py sdist bdist_wheel
python -m twine upload dist/*
popd