# Thorlabs Power Measurement

The thorlabs PM100D is a USBTMC device.

## Installation

```bash
sudo usermod -aG plugdev $USER
```

```bash
sudo tee /etc/udev/rules.d/99-thorlabs.rules > /dev/null << 'EOF'
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1313", GROUP="plugdev", MODE="0666"
EOF
```

Reload udev rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

```
pip install git+https://github.com/ElTinmar/python-usbtmc pyvisa pyusb libusb-package
```

## Communication

via usbtmc

```
import usbtmc
instr = usbtmc.Instrument(0x1313,0x8078)
instr.write("SENS:CORR:WAV 500")
print(instr.ask("MEAS:POW?"))
```

To use Python USBTMC in Windows, PyUSB and libusb are required. They can be downloaded from:

    http://sourceforge.net/projects/pyusb/
    http://www.libusb.org/wiki/libusb-win32

An INF file will also need to be created in order to use devices with libusb. Without a properly set up INF file, Python USBTMC will not be able to locate the device. There are instructions on the libusb page for how to generate the INF file.


via pyvisa

```
import usb.core
import pyvisa



rm = pyvisa.ResourceManager()
print(rm.list_resources())
instr = rm.open_resource('USB0::0x1313::0x8078::P0009368::INSTR')
instr.query("MEAS:POW?")
```


## Useful references

https://github.com/Thorlabs/Light_Analysis_Examples/tree/main/Python/Thorlabs%20PMxxx%20Power%20Meters/scpi


'The analogue bandwidth setting influences the power reading and the
analogue output. The bandwidth can be selected in the Meas Config measurement
configuration menu to ‘HI’ (range dependent bandwidth up to 100 kHz) or ‘LO’ (15 Hz
bandwidth) by toggling the BW H I /LOW button.
For measuring CW or average power from pulsed sources the bandwidth should
be set to ‘LO’'