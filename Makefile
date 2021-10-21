DIST=./dist

build:
		mkdir $(DIST)
		cp -r app $(DIST)
		cp Dockerfile $(DIST)
		cp -r run.py mibs main.py Pip* $(DIST)
		ls -la $(DIST)
		cd $(DIST) && docker build --rm -t snmpscustom:v1 .

clean:
		rm -rf $(DIST)