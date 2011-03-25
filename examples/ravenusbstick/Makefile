all:
	${MAKE} TARGET=avr-ravenusb NOAVRSIZE=1 -f Makefile.ravenusbstick ravenusbstick.elf
	avr-objcopy -O ihex -R .signature -R .fuse -R .eeprom ravenusbstick.elf ravenusbstick.hex
	avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom="alloc,load" --change-section-lma .eeprom=0 ravenusbstick.elf ravenusbstick_eeprom.hex
	avr-size -C --mcu=at90usb1287 ravenusbstick.elf

prog:
	avrdude -p usb1287 -c dragon_jtag -P usb -U flash:w:ravenusbstick.hex:i -U eeprom:w:raven_usbstick_eeprom.hex:i


clean:
	${MAKE} -f Makefile.ravenusbstick clean
	rm -rf obj_avr-ravenusb
	rm symbols.c symbols.h ravenusbstick.elf ravenusbstick.hex
