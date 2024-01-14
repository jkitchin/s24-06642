build:
	jupyter book build dsmles

open:
	open dsmles/_build/html/index.html

clean:
	jupyter book clean dsmles

deploy:
	ghp-import -n -p -f dsmles/_build/html

gh:
	open https://github.com/jkitchin/dsmles

web:
	open https://kitchingroup.cheme.cmu.edu/dsmles

pdf:
	jupyter-book build dsmles/ --builder pdfhtml
