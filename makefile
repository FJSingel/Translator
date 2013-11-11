all: translator

translator: translator.py
	python -m compileall translator.py
	python -m compileall basic_tests.py

test: basic_tests.py
	python basic_tests.py -v -x stress

stresstest: basic_tests.py
	python basic_tests.py -v -i stress

clean:
	rm *.pyc
