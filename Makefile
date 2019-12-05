PELICAN_SETTINGS ?= pelicanconf.py

all: build

clean:
	rm -rf build/*
	mkdir -p build

grunt:
	./node_modules/grunt/bin/grunt -v

pelican:
	pelican -o build -s $(PELICAN_SETTINGS)

build: grunt pelican

serve:
	cd build && python3 -m http.server --bind 127.0.0.1 8080
