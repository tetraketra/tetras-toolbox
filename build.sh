rm -f dist/*
rm -f tetras_toolbox.egg-info
/bin/python3 -m pip install .
/bin/python3 -m build
/bin/python3 -m twine upload --verbose dist/*