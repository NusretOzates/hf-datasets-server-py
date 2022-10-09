all: isort reformat test pypi

isort:
	isort .

reformat:
	black .

test:
	pytest .

pypi:
	python setup.py sdist bdist_wheel
	twine upload dist/* -u ${PYPI_USER} -p ${PYPI_PASSWORD}