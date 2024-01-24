default: install

install:
	mkdir -pv $HOME/.local/bin
	cp src/main.py $HOME/.local/bin/buckshot-cli

systeminstall:
	sudo cp src/main.py /usr/bin/buckshot-cli

uninstall:
	rm $HOME/.local/bin/buckshot-cli

systemuninstall:
	sudo rm /usr/bin/buckshot-cli
