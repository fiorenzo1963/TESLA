all:
	@echo nothing to do for all yet

clean:
	-killall -9 tesla_data_collector.py
	/bin/rm -f */*pyc
	/bin/rm -rf */__pycache__

install_required_libs:
	sudo pip3 install python-daemon
	sudo pip3 install requests
