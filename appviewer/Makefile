# This makefile shall help to : 
# build the c++ demo sinusoid
# create python venv 
# run demo :
# mode 1


all: help

# install python vend & build
install: .venv sinusoid
	@echo "Installation complete. type make run to start the demo."

# build the c++ demo
sinusoid: sinusoid.cpp Makefile
	# whatis is important is "-"g", the process can be opimtized.
	g++ -g -O0 -Wall -Wextra sinusoid.cpp -o sinusoid


# create python venv and install dependencies
.venv : requirements.txt
	python3 -m venv .venv 
	. .venv/bin/activate ; pip install -r requirements.txt  

# run the demo and open the web browser client
run: sinusoid
	./sinusoid & echo $$! > sinusoid.pid
	sudo .venv/bin/python sinusoid_monitor.py & echo $$! > sinusoid_monitor.pid
	@echo "Waiting for server to start..."
	sleep 2
	@echo "Opening web browser..."
	xdg-open http://localhost:8050

# stop the demo - FIXME: this is not working properly
stop: 
	sudo pkill -f sinusoid_monitor.py --signal 9 || true
	@if [ -f sinusoid.pid ]; then \
		kill -9 $$(cat sinusoid.pid) || true; \
		rm -f sinusoid.pid; \
	else \
		echo "No sinusoid.pid file found. sinusoid process may not be running."; \
	fi

help: Makefile
	@echo "Available targets:"
	@sed -n -e '/^#/ {s/^# *//; h; n; /^[a-zA-Z0-9_.-]\+:/ {s/:.*//; G; s/\n/ : /; p}}' $<

#  test the generic memory proxy functionality : list variables in the elf file
test_memproxy: .venv
	@echo "Test listing variables."
	. .venv/bin/activate ; python procmemproxy.py --elf sinusoid --listvars
	@echo "Launching sinusoid for read/write test."
	@./sinusoid & echo $$! > sinusoid.pid;
	@echo "test reading/writing variable 'run' in sinusoid process."
	@sudo .venv/bin/python ./procmemproxy.py --elf sinusoid --read run int ; \
	sudo .venv/bin/python ./procmemproxy.py --elf sinusoid --write run int 0; \
	sudo .venv/bin/python ./procmemproxy.py --elf sinusoid --read run int;
	@if [ -f sinusoid.pid ]; then \
		kill -9 $$(cat sinusoid.pid) || true; \
		rm -f sinusoid.pid; \
	else \
		echo "No sinusoid.pid file found. sinusoid process may not be running."; \
	fi
	@echo "Test complete. try memory proxy with --read and --write options."

#  test the sinusoid proxy functionality : list variables in the elf file
test_sinusoid_proxy: .venv
	@echo "Launching sinusoid for read/write test."
	@./sinusoid & echo $$! > sinusoid.pid;
	@echo "test reading/writing variable 'run' in sinusoid process."
	@sudo .venv/bin/python ./sinusoid_memproxy.py --elf sinusoid --read XY ; \
	sudo .venv/bin/python ./sinusoid_memproxy.py --elf sinusoid --read run ; \
	sudo .venv/bin/python ./sinusoid_memproxy.py --elf sinusoid --read A ;
	@if [ -f sinusoid.pid ]; then \
		kill -9 $$(cat sinusoid.pid) || true; \
		rm -f sinusoid.pid; \
	else \
		echo "No sinusoid.pid file found. sinusoid process may not be running."; \
	fi
	@echo "Test complete. try sinusoid proxy with --read and --write options."

.PHONY: stop
