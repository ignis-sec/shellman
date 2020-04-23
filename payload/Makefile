CC		:= g++
C_FLAGS := -std=c++17 -Wall -Wextra -g -fpermissive
RCC := rcc-qt5


BIN		:= bin
SRC		:= src
INCLUDE	:= include
LIB		:= lib
RES		:= $(wildcard resources/*)
LIBRARIES	:=


ifeq ($(OS),Windows_NT)
EXECUTABLE	:= shell.exe
else
EXECUTABLE	:= shell
endif


%.rc: $(RES)
    $(file > $@.rc, $^)

all: $(BIN)/$(EXECUTABLE)

clean:
	$(RM) $(BIN)/$(EXECUTABLE)

run: all
	./$(BIN)/$(EXECUTABLE)

$(BIN)/$(EXECUTABLE): $(SRC)/*
	$(CC) $(C_FLAGS) -I$(INCLUDE) -L$(LIB) $^ -o $@ $(LIBRARIES)