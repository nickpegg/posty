develop:
	pip install -r requirements.dev.txt
	pip install -e .

test:
	pycodestyle posty tests
	flake8 posty tests
	pytest
