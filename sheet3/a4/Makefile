KDIR := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

obj-m := rootkit.o

all:
	@echo $(KDIR)
	@echo $(PWD)
	make -C $(KDIR) M=$(PWD) modules

clean:
	make -C $(KDIR) M=$(PWD) clean
