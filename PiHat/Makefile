OUTPUT_DIRECTORY := build
SRC_DIRECTORY := src

all: profiler

profiler: ina219.so
	g++ -o $(OUTPUT_DIRECTORY)/profiler $(SRC_DIRECTORY)/ina219.cc profiler.cc


ina219.so:
	mkdir -p $(OUTPUT_DIRECTORY)
	g++ -o $(OUTPUT_DIRECTORY)/ina219.so -c $(SRC_DIRECTORY)/ina219.cc

# install:
# 	cp ./build/ina219.so $(PREFIX)

# uninstall:


clean:
	rm -rf $(OUTPUT_DIRECTORY)/*

.PHONY: $(OUTPUT_DIRECTORY) $(SRC_DIRECTORY)
