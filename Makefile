CC=gcc
CFLAGS=-Wall

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

i2cwrite: i2cwrite.o
	$(CC) -o i2cwrite i2cwrite.o

all: i2cwrite
