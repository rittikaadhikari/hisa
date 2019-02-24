PYTHON = python

install:
	cat requirements/*.txt > requirements.txt
	pip install -r requirements.txt

	pip install tensorflow-gpu

	$(PYTHON) setup.py install

	#bash twitter.sh

clean:
	$(PYTHON) setup.py clean

all:
	make install clean
