# PatrowlAssets


# Pypi Deployment commands
rm -rf dist/ build/ PatrowlAssets.egg-info
python3 setup.py sdist bdist_wheel
twine upload -u Patrowl dist/*
