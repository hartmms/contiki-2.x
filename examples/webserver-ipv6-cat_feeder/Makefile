TARGET=avr-atmega128rfa1
MCU=atmega128rfa1
WEBDIR=cat_feeder
PCB = LIGHT_SW_PCB_R1=1
#PCB = BLIND_PCB_R0=1
#PCB = XBEE_PCB_R1=1

ifndef WEBDIR
 OUTFILE=webserver6-$(TARGET)
else
 OUTFILE=webserver6-$(WEBDIR)-$(TARGET)
endif

$(OUTFILE).hex: all
all:
	${MAKE} -f Makefile.webserver TARGET=$(TARGET) WEBDIR=$(WEBDIR) DEFINES=$(PCB) NOAVRSIZE=1 webserver6.elf   
#can't just rename, webserver6 may be open in debugger
	@if [ $(OUTFILE) != "webserver6" ]; then cp webserver6.elf $(OUTFILE).elf;fi
	avr-objcopy -O ihex -R .eeprom -R .fuse -R .signature $(OUTFILE).elf $(OUTFILE).hex
	avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom="alloc,load" --change-section-lma .eeprom=0 $(OUTFILE).elf $(OUTFILE)_eeprom.hex
	avr-size -C --mcu=$(MCU) $(OUTFILE).elf

prog: $(OUTFILE).hex
	avrdude -V -p $(MCU) -c dragon_isp -P usb -U flash:w:$(OUTFILE).hex:i -U eeprom:w:$(OUTFILE)_eeprom.hex:i

clean:
	${MAKE} -f Makefile.webserver TARGET=$(TARGET) clean
	rm /media/av/ep/6loWpan/contiki-2.x/platform/avr-atmega128rfa1/apps/raven-webserver/httpd-fsdata.c
	rm symbols.c symbols.h webserver6.elf $(OUTFILE).elf  *.hex
	rm -rf obj_avr-raven
