init: 
	pip3 install -r ./requirements/stage1.txt
	pip3 install -r ./requirements/stage2.txt

test:
	pytest --cov=./ --junitxml=test-reports/junit.xml --html=test-reports/pytest_report.html --self-contained-html tests/test.py

package:
	python3 setup.py sdist bdist_wheel
	twine check dist\*
