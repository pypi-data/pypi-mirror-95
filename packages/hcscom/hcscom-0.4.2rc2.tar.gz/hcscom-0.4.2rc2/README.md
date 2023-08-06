# hcscom

A python3 class for remote control of manson hcs lab power supplies.

Manson lab power supply units can be controlled via usb.

Communication is done via a builtin CP210x usb-serial bridge and 8N1@9600 port settings.


# clones

Several PeakTech brand devices seem to be clones of Manson devices, i.e.

https://www.peaktech.de/productdetail/kategorie/schaltnetzteile/produkt/p-1575.html

https://www.manson.com.hk/product/hcs-3402-usb/

The command set and even the parts of the documentation are identical while the Manson documentation has slightly more details at technical sections.

The command `GMOD` can be used to find out the device model. Apparently it is omitted in the documentation to obscure the device manufacturer.
