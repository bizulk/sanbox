sinusoid: sinusoid.cpp Makefile
	g++ -g -O0 -Wall -Wextra sinusoid.cpp -o sinusoid

all: sinusoid

run: sinusoid
	./sinusoid
	echo "sudo $(which python3) sinusoid_monitor.py"

.venv: 
	python3 -m venv .venv

venv : requirements.txt .venv
	echo source .venv/bin/activate

