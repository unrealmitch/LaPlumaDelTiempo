FUENTE = main

all: run

run:
	python ./Game/$(FUENTE).py 

clean:
	rm -f *.pyc

