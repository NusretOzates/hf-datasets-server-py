all: isort reformat test pypi

isort:
	isort .

reformat:
	black .

test:
	pytest .

push:
	git config user.name github-actions
	git config user.email github-actions@github.com
	git add .
	git commit -m "Auto Formatted"
	git push

pypi:
	python setup.py bdist_wheel
	twine upload dist/* -u ${PYPI_USER} -p ${PYPI_PASSWORD}