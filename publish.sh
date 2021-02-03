pip3 install setuptools wheel twine
pushd src
rm -rf dist/
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
popd