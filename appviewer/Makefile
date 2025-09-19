sinusoid: sinusoid.cpp Makefile
	g++ -g -O0 -Wall -Wextra sinusoid.cpp -o sinusoid

all: sinusoid

.venv : requirements.txt
	python3 -m venv .venv 
	. .venv/bin/activate ; pip install -r requirements.txt  

run: sinusoid
	./sinusoid & echo $$! > sinusoid.pid
	sudo .venv/bin/python sinusoid_monitor.py & echo $$! > sinusoid_monitor.pid
	@echo "Waiting for server to start..."
	sleep 2
	@echo "Opening web browser..."
	xdg-open http://localhost:8050

stop: 
	sudo pkill -f sinusoid_monitor.py --signal 9 || true
	@if [ -f sinusoid.pid ]; then \
		kill -9 $$(cat sinusoid.pid) || true; \
		rm -f sinusoid.pid; \
	else \
		echo "No sinusoid.pid file found. sinusoid process may not be running."; \
	fi

.PHONY: stop
