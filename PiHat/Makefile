OUTPUT_DIRECTORY := build
SRC_DIRECTORY := src

all: profiler

profiler: ina219
	g++ -o $(OUTPUT_DIRECTORY)/$@.o -c $@.cc
	g++ $(OUTPUT_DIRECTORY)/$@.o -o $(OUTPUT_DIRECTORY)/$@ -L$(OUTPUT_DIRECTORY) -l$<

ina219:
	mkdir -p $(OUTPUT_DIRECTORY)
	g++ -o $(OUTPUT_DIRECTORY)/$@.o -c $(SRC_DIRECTORY)/$@.cc
	ar rcs $(OUTPUT_DIRECTORY)/lib$@.a $(OUTPUT_DIRECTORY)/$@.o

clean:
	rm -rf $(OUTPUT_DIRECTORY)/*

.PHONY: $(OUTPUT_DIRECTORY) $(SRC_DIRECTORY)
