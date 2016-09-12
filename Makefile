PELICAN_SETTINGS ?= pelicanconf.py

clean:
	rm -rf build/*
	mkdir -p build

grunt:
	./node_modules/grunt-cli/bin/grunt -v

pelican:
	pelican -o build -s $(PELICAN_SETTINGS)

build: grunt pelican

serve:
	cd build && python -m http.server 8080
