PYTHON = python

install:
	cat requirements/*.txt > requirements.txt
	pip install -r requirements.txt

	$(PYTHON) setup.py install

clean:
	$(PYTHON) setup.py clean

all:
	make install clean
