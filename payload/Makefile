CC		:= g++
C_FLAGS := -std=c++17 -Wall -Wextra -g -fpermissive
RCC := rcc-qt5


BIN		:= bin
SRC		:= src
INCLUDE	:= include
LIB		:= lib

LIBRARIES	:=


ifeq ($(OS),Windows_NT)
EXECUTABLE	:= shell.exe
else
EXECUTABLE	:= shell
endif


$(shell xxd -i resources/socat > src/socat.h)
$(shell xxd -i ../cert.pem > src/cert.h)

all:$(BIN)/$(EXECUTABLE)

clean:
	$(RM) $(BIN)/$(EXECUTABLE)

run: all
	./$(BIN)/$(EXECUTABLE)

$(BIN)/$(EXECUTABLE): $(SRC)/*
	$(CC) $(C_FLAGS) -I$(INCLUDE) -L$(LIB) $^ -o $@ $(LIBRARIES)
