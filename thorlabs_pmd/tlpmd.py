import usb.core
import usbtmc
import sys
from typing import List, NamedTuple, Tuple


if sys.platform == 'win32':
    import libusb_package
    libusb_backend = libusb_package.get_libusb1_backend()
else:
    libusb_backend = None

class DeviceNotFound(Exception): ...

THORLABS_VID = 0x1313
PM100D_PID = 0x8078
LINE_FREQUENCY_EUROPE = 50
S120C_APERTURE_SIZE_MM = 9.5
PID_RANGE = (0x8078, 0x8079) # TODO check actual values
area = 3.14159 * (S120C_APERTURE_SIZE_MM/2)**2

# S120C 
# Active Detector Area 	9.7 mm x 9.7 mm
# Aperture Size 	Ø9.5 mm
# to display the power or energy density or the light intensity value in W/cm² or
# J/cm² in the right sub display it is necessary to enter the diameter of the incident
# beam or at an overfilled sensor the diameter of the sensor aperture.

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
        self.initialize()
        
    def initialize(self): 
        self.instr.write("*CLS")
        self.instr.write("SENS:POW:RANGE:AUTO ON")
        self.instr.write("SENS:POW:UNIT W")
        self.instr.write("SENS:AVER 1000")

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
    
    def get_beam_diameter_mm(self) -> float:
        return float(self.instr.ask("SENS:CORR:BEAM?"))
    
    def set_beam_diameter_mm(self, diameter: float) -> None:
        self.instr.write(f"SENS:CORR:BEAM {diameter}")
        self.check_error_code()
        
    def get_wavelength_nm(self) -> float:
        return float(self.instr.ask(f"SENS:CORR:WAV?"))

    def set_wavelength_nm(self, wavelength: float) -> None:
        self.instr.write(f"SENS:CORR:WAV {wavelength}")
        self.check_error_code()

    def get_power_mW(self) -> float:
        power = self.instr.ask("MEAS:POW?")
        return float(power)*10**3
    
    def get_power_density_mW_cm2(self) -> float:
        beam_diameter_cm = self.get_beam_diameter_mm() * 0.1
        area_cm2 = 3.14159 * (beam_diameter_cm/2)**2
        return self.get_power_mW()/area_cm2

    def clear(self) -> None:
        self.instr.clear()
        
    def reset(self) -> None:
        self.instr.write(f"*RST")

    def close(self) -> None:
        self.instr.close()

if __name__ == '__main__':

    powermeters = list_powermeters()
    dev = TLPMD(powermeters[0])
    dev.set_wavelength_nm(550)
    print(dev.get_power_density_mW_cm2())
    dev.close()