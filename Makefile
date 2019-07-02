all: html

html:
	cd tests && make html

pdf:
	cd tests && make pdf

docx:
	cd tests && make docx

clean:
	cd tests && make clean

init:
	cd tests && make init

install:
	pip3 install .

uninstall:
	pip3 uninstall pandoc-pandocker-filters

reinstall: uninstall install
