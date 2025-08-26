# TLCCS library

This is an attempt to use Thorlab's NI-VISA based library directly on linux.
So far I could not get this to work.
Use the pyusb re-implementation in the root directory instead.

## Dependencies

https://www.ni.com/de/support/downloads/drivers/download.ni-visa.html
extract downloaded archive

```bash
sudo apt install ./ni-ubuntu2404-drivers-2025Q3.deb
sudo apt update
sudo apt upgrade
sudo apt install ni-visa ni-visa-devel
```

## Build library
gcc -fPIC -shared TLCCS.c -o libtlccs.so -I/usr/include/ni-visa -L/usr/lib/x86_64-linux-gnu -lvisa