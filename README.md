# CT800-PCB

In order to become familiar with KiCAD and making something useful at the same time I started this project. The goal was to develop a PCB for the CT800 to ease the build-up. The CT800 is a dedicated chess computer made by Rasmus Althoff. It is very well documented, take a look at its homepage [www.ct800.net](https://www.ct800.net "CT800 Homepage") for detailed info. 

The developed PCB consists entirely of THT components except one SMD transistor, due to better availability of 3.3V logic level devices. Soldering SMD parts isn’t easy especially packages like LQFP64 with 0.5mm pitch, therefore the Olimex board was kept in this design. The CT800 was extended by some interfaces (RS232, Bluetooth, WLAN) for future use. The power supply was amended a bit too.

CAD files of appropriate panels for housings are also included in this project. There are two versions:

* the Spartan one consists of front and back panel which are bolted to the PCB by studs
* the Classic one consists of just a front panel for the housing used by Rasmus (Axxatronic BIM1006-BLK/PG or BIM1006-GY/PG)

These panels are intended to be transparent, hence there are no holes for display and LEDs. Due to transparency there is no need for additional button labels.

## Project Data

* __CT800_PCB__ directory contains the KiCAD project including project specific libs and footprints as well gerber files for PCB production

* __CT800_PANEL__ directory contains panels (in KiCAD layout and SVG formats) for different housings

* __gen_panel_acrylic.py__ Python script for generating panel layouts from PCB layout

* __bom.txt__ lists the bill of material, mounting material for panels not included (M3x8mm / M3x25mm studs, washers, bolts...)

## Power Supply

Depending on assembly the CT800 can be powered by different sources: 

* by a 5V source on the USB-A connector 
* by power adopter or external battery on the barrel jack
	* 8-12VDC if the 7805 voltage regulator is used 
	* 4-12VDC if the Pololu S9V11F5 is used
* by internal battery if a switch is used


The USB-B connector on the Olimex board is not intended for powering the CT800 but for USB devices like a sensor chessboard. So __don’t feed the CT800 via USB-B connector.__

__Don’t provide power from multiple sources simultaneously to the CT800 in general. This could lead to side effects or even damage!__

In order to feed the CT800 by low voltage power supply down to 4VDC  (e.g. battery) equip the PCB with the Pololu S9V11F5 voltage regulator (or similar 5V buck/boost converter) instead of the 7805. In this context replacing the 1N4007 diode by a Schottky type (e.g. 1N5818, SB130) is recommended for higher efficiency.

The CT800 firmware provides voltage monitoring for four NiMH (or alkaline) cells connected in serial, in order to protect rechargeable batteries from deep discharge. This only makes sense in conjunction with the Pololu regulator. Dispense with this monitoring eases the build-up, so omit it unless you really need it. To do so, omit the voltage divider components (R2, R3 and C1), instead connect the R2 pad next to C1 to 3.3V (red wire on ct800_spartan_bottom.jpg).

A power switch is not provided on the PCB but can be connected easily to PWR and USB_SEL pads.

### Operating Without Power Switch

The CT800 is immediately powered by plugging a 5V supply to the USB-A connector or a “wide range” power source to the barrel jack (8-12VDC or 4-12VDC depending on the used 5V regulator).

If battery monitoring is active (thus the Pololu is used), the USB power has to be redirected to 5V regulator’s input via the USB_SEL jumper: disrupt the connection on top side between the upper two pads and short-circuit the lower two. Otherwise powering via USB will result in “low batteries” error message. Because of this redirection the power adopter (or battery) is directly connected to the USB power supply. __Despite the fuses, this easily lead to damage in case two power sources are used simultaneously!__ Therefore use a switch instead or dispense with battery monitoring.

### Operating With Power Switch

Without battery monitoring a 2x3 pin toggle switch is sufficient to switch between USB-A and barrel jack supply. An external battery can still be used on the barrel jack. If internal battery is desired a 1x4 rotary switch is recommended for supply selection. Wire the switch as shown in the picture below, don’t forget to disrupt the red marked traces on the PCB.

![switch](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_switch.jpg)

Many other switch configurations are possible. Whatever you choose, ensure power sources are never short circuit!

## PCB Assembly

Read the entire text before starting assembly. Decide what power source you want to use for feeding the CT800 and if you need a power switch or not. Since the ESP-01 is not used yet by the firmware, there is no need for equipping it. This just leads to higher current consumption. It is recommended to place the smallest components first: the SMD transistor, resistors, capacitors and then the remaining parts but the display and Olimex board. Consider the polarity of diodes, LEDs (cathode to rectangular pad = ground) and polarized capacitors. Apply heat paste to the voltage regulator(s) and screw them to the PCB before soldering. If battery monitoring is used, activate the JP3 jumper on top side. Before placing display and Olimex board check the 5V and 3.3V voltages (there are test points on the PCB). __Don’t proceed until these voltages are alright.__ Before soldering the display, screw it to the PCB and adjust the height by putting washers in between. On some displays the polarity of the back light has to be changed. On the back side of the display are jumpers for this purpose, regard the data sheet. __Don’t solder the Olimex board to the PCB, use female header instead.__ For UART communication between µC and ESP-01 the resistor R27 on the Olimex board has to be removed. In order to prevent the gold-cap to be drained in off state, the VBAT jumper on the STM32H405 board has to be disrupted. 

## Schematic

![schematic](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_schematic.png)

## PCB

![pcb_top](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_rev2_top.jpg)

![pcb_bottom](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_rev2_bottom.jpg)

## Spartan Housing

![spartan_top](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_spartan_top.jpg)

![spartan_bottom](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_spartan_bottom.jpg)

## Classic Housing

![classic_top](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_classic_top.jpg)
![classic_back](https://github.com/d3rvita/ct800-pcb/blob/master/pics/ct800_classic_back.jpg)

