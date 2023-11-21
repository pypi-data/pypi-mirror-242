rm -rf dist
mkdir dist
python3 -m build

echo '__token__'
echo 'pypi-AgENdGVzdC5weXBpLm9yZwIkMDk5MGIyNmMtMTA4ZC00NjVlLTg3YmUtMWQ0Y2ViNGE0OTQ0AAIqWzMsImYyYzc3MjdiLWZiZjItNGM4MS04YzllLTA5OGQ3OWQzZmI0YyJdAAAGIDlCUPblbnCCB8T02xB07RUP5bpTuivSvLooFh5-5sJZ'
python3 -m twine upload --repository testpypi dist/* --verbose
