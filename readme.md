# specelUFC
This is a software designed to put all information from DCS:FA18C Hornet's Up Front Controller (UFC) to Logitech G-series keyboards. Developed for **Logitech G13**, but should also work with any other Logitech device with 160x43 px monchrome display, like G15 and G510.

## Requirements
* Installed Logitech Gaming Software https://support.logitech.com/software/lgs

* Installed Logitech LCD SDK_8.57.148 in `C:\Program Files\Logitech Gaming Software\LCDSDK_8.57.148` http://gaming.logitech.com/sdk/LCDSDK_8.57.148.zip

* DCS-BIOS https://github.com/dcs-bios/dcs-bios copied into `C:\Users\XXX\Saved Games\DCS.openbeta\Scripts`. You also need to add `dofile(lfs.writedir()..[[Scripts\DCS-BIOS\BIOS.lua]])` line to your `C:\Users\XXX\Saved Games\DCS.openbeta\Scripts\Export.lua` file

* Installed DCS-BIOS F/A-18C library `https://forums.eagle.ru/showthread.php?t=210960` by AndrewW for DCS-BIOS (just copy into DCS-BIOS Scripts folder)

## Credits
This software uses:
* https://github.com/dcs-bios/dcs-bios DCS-BIOS for exporting data from DCS to local network
* https://github.com/jboecker/python-dcs-bios-example jboecker's parser to read data stream from DCS-BIOS
* https://github.com/50thomatoes50/GLCD_SDK.py A Python wrapper for Logitech's LCD SDK

## Usage
* First, you need to "subscribe" data you want and pass it to G13Handler: 
```ScratchpadNumberDisplay = StringBuffer(parser, 0x543e, 8, lambda s: g13.setData(3,s))```
For required adress and data length look up in `C:\Users\XXX\Saved Games\DCS.openbeta\Scripts\DCS-BIOS\doc\control-reference.html`
* Then, use parser 
	c = s.recv(1)
	parser.processByte(c)
which callback function in G13Handler `setData` with apropriate paramteres and update display content, by creating bitmap and passing it through LCD SDK to device display
* You can also use 4 button below display, just check with `g13.checkButtons()` whitch one ise pressed and send TCP packet with command you wish to use. Again, look it up in `control-reference.html`, for example `s.send(bytes("UFC_COMM1_CHANNEL_SELECT -3200\n","utf-8"))` to rotate COMM1 knob left






