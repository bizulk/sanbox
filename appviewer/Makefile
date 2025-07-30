sinusoid: sinusoid.cpp Makefile
	g++ -g -O0 -Wall -Wextra sinusoid.cpp -o sinusoid

all: sinusoid

run: sinusoid
	sudo $(which python3) sinusoid_monitor.py
