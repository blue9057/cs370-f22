TARGET := launcher
CFLAGS := -Wno-unused-result -g -O2

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -rf $(TARGET)
