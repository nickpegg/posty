test:
	pycodestyle posty tests
	flake8 posty tests
	pytest
