import usb.core
import usbtmc
import sys
from typing import List, NamedTuple

if sys.platform == 'win32':
    import libusb_package
    libusb_backend = libusb_package.get_libusb1_backend()
else:
    libusb_backend = None

REN_CONTROL = 160 # Optional. Mechanism to enable or disable local controls on a device.
GO_TO_LOCAL = 161 # Optional. Mechanism to enable local controls on a device. 
THORLABS_VID = 0x1313
PID_RANGE = (0x8078, 0x8079) # TODO check actual values

class DevInfo(NamedTuple):
    vid: int
    pid: int
    serial_number: str

def list_powermeters() -> List[DevInfo]:
    
    devices = usb.core.find(
        idVendor = THORLABS_VID, 
        backend = libusb_backend, 
        custom_match = lambda d: d.idProduct in range(*PID_RANGE),
        find_all = True
    )

    res = []
    for dev in devices:
        res.append(DevInfo(
            vid = dev.idVendor,
            pid = dev.idProduct,
            serial_number = dev.serial_number 
        ))

    return res

class TLPMD:

    def __init__(
            self,
            device_info: DevInfo,
        ) -> None:
        
        self.instr = usbtmc.Instrument(device_info.vid, device_info.pid, device_info.serial_number)
        self.instr.clear = lambda: None
        self.instr.open()
        self.remote_enable(1)
        self.initialize()
        
    def initialize(self): 
        self.instr.write("*CLS;*SRE 0;*ESE 0;:STAT:PRES")
        self.check_error_code()
        self.instr.write("ABOR")
        self.instr.write("CONF:POW")
        self.instr.write("SENS:AVER:COUN 1")
        # self.instr.ask("INP:FILT?")
        # self.instr.write("INP:FILT ON") # which syntax?
        # self.instr.write("INP:PDI:FILT:LPAS:STAT ON") # set LO (15Hz) bandwidth mode
        self.check_error_code()

    def remote_enable(self, value: int) -> None:
        self.instr.device.ctrl_transfer(bmRequestType=0xA1, bRequest=REN_CONTROL, wValue=value, wIndex=0x0000, data_or_wLength=1)

    def local_control(self) -> None:
        self.instr.device.ctrl_transfer(bmRequestType=0xA1, bRequest=GO_TO_LOCAL, wValue=0x0000, wIndex=0x0000, data_or_wLength=1)

    def check_error_code(self) -> None:
        error = self.instr.ask("SYST:ERR?")
        code, descr = error.split(',', 1)
        code, descr = int(code), descr.strip('"')
        if code != 0:
            raise RuntimeError(f'Error code {code}: {descr}')

    def get_line_frequency_Hz(self) -> float:
        return float(self.instr.ask(f"SYST:LFR?"))

    def set_line_frequency_Hz(self, line_frequency: float) -> None:
        self.instr.write(f"SYST:LFR {line_frequency}")
        self.check_error_code()

    def get_beam_diameter_mm(self) -> float:
        return float(self.instr.ask("SENS:CORR:BEAM?"))
    
    def set_beam_diameter_mm(self, diameter: float) -> None:
        self.instr.write(f"SENS:CORR:BEAM {diameter}")
        self.check_error_code()

    def get_max_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV? MAX"))
    
    def get_min_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV? MIN"))
    
    def get_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV?"))

    def set_wavelength_nm(self, wavelength: float) -> None:
        self.instr.write(f"SENS:CORR:WAV {wavelength}")
        self.check_error_code()

    def get_power_mW(self) -> float:
        power = self.instr.ask("Read?")
        return float(power)*10**3
    
    def get_power_density_mW_cm2(self) -> float:
        beam_diameter_cm = self.get_beam_diameter_mm() * 0.1
        area_cm2 = 3.14159 * (beam_diameter_cm/2)**2
        return self.get_power_mW()/area_cm2

    def close(self) -> None:
        self.local_control()
        self.remote_enable(0)
        self.instr.close()
        self.instr = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':

    powermeters = list_powermeters()
    dev = TLPMD(powermeters[0])
    dev.set_wavelength_nm(550)
    print(dev.get_power_density_mW_cm2())
    dev.close()