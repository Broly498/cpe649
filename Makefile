TARGETS := all clean

PI_HAT_SUBDIRECTORY := PiHat

$(TARGETS): $(PI_HAT_SUBDIRECTORY)
$(PI_HAT_SUBDIRECTORY):
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TARGETS) $(PI_HAT_SUBDIRECTORY)
